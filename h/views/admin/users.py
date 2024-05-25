import datetime
import deform
from markupsafe import Markup
from pyramid import httpexceptions
from pyramid.view import view_config, view_defaults
from sqlalchemy import func, case

from h import models, paginator
from h.accounts.events import ActivationEvent
from h.i18n import TranslationString as _
from h.schemas.forms.admin.signup import RegisterSchema
from h.security import Permission
from h.services.user_rename import UserRenameError
from h.services.exceptions import ConflictError


class UserNotFoundError(Exception):
    pass


def format_date(date):
    """Format a date for presentation in the UI."""

    if date is None:
        return ""

    # Format here is "2012-01-29 21:19"
    return date.strftime("%Y-%m-%d %H:%M")


@view_config(
    route_name="admin.users",
    request_method="GET",
    renderer="h:templates/admin/users.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
def users_index(request):
    user = None
    user_meta = {}
    username = request.params.get("username")
    authority = request.params.get("authority")

    if username:
        username = username.strip()
        authority = authority.strip()
        user = models.User.get_by_username(request.db, username, authority)
        if user is None:
            user = models.User.get_by_email(request.db, username, authority)

    if user is not None:
        svc = request.find_service(name="annotation_stats")
        user_meta["annotations_count"] = svc.total_user_annotation_count(user.userid)

    return {
        "default_authority": request.default_authority,
        "username": username,
        "authority": authority,
        "user": user,
        "user_meta": user_meta,
        "format_date": format_date,
    }


@view_config(
    route_name="admin.batch_users",
    request_method="GET",
    renderer="h:templates/admin/batch_users.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
def batch_users(request):
    username = request.params.get("username")

    users = []
    filter_terms = []
    if username and len(username) >= 3:
        filter_terms.append(func.lower(models.User.username).like(f"%{username.lower()}%"))
        users = request.db.query(models.User) \
            .filter(*filter_terms) \
            .all()

    return {
        "users": users,
        "format_date": format_date,
    }


@view_defaults(
    route_name="admin.users_create",
    permission=Permission.AdminPage.LOW_RISK,
)
class UserCreateController:
    def __init__(self, request):
        self.request = request
        # self.username = request.params.get("username")
        # self.email = request.params.get("email")
        # self.registration = self.registration_service.get_by_id(registration_id)
        self.schema = RegisterSchema().bind(request=self.request)
        self.form = request.create_form(
            self.schema,
            buttons=(deform.Button(title=_("Sign up")),),
            # css_class="js-disable-on-submit",
        )

    @view_config(
        request_method="GET",
        renderer="h:templates/admin/users_create.html.jinja2",
    )
    def get(self):
        return {"form": self.form.render()}

    @view_config(
        request_method="POST",renderer="h:templates/admin/users_create.html.jinja2"
    )
    def post(self):
        try:
            appstruct = self.form.validate(self.request.POST.items())
        except deform.ValidationFailure:
            return {"form": self.form.render()}

        signup_service = self.request.find_service(name="user_signup")

        template_context = {"heading": _("Account registration successful")}
        try:
            signup_service.signup(
                username=appstruct["username"],
                email=appstruct["email"],
                password=appstruct["username"],
                privacy_accepted=datetime.datetime.utcnow(),
                comms_opt_in=True,
            )
        except ConflictError as exc:
            template_context["heading"] = _("Account already registered")
            template_context["message"] = _(
                # pylint:disable=consider-using-f-string
                "{failure_reason}".format(failure_reason=exc.args[0])
            )

        return template_context

    def _template_context(self):
        return {
            "form": self.form.render(),
        }


@view_config(
    route_name="admin.users_activate",
    request_method="POST",
    request_param="userid",
    permission=Permission.AdminPage.LOW_RISK,
    require_csrf=True,
)
def users_activate(request):
    user = _form_request_user(request)

    user.activate()

    request.session.flash(
        # pylint:disable=consider-using-f-string
        Markup(_("User {name} has been activated!".format(name=user.username))),
        "success",
    )

    request.registry.notify(ActivationEvent(request, user))

    return httpexceptions.HTTPFound(
        location=request.route_path(
            "admin.users",
            _query=(("username", user.username), ("authority", user.authority)),
        )
    )


@view_config(
    route_name="admin.users_rename",
    request_method="POST",
    permission=Permission.AdminPage.LOW_RISK,
    require_csrf=True,
)
def users_rename(request):  # pragma: no cover
    user = _form_request_user(request)

    old_username = user.username
    new_username = request.params.get("new_username").strip()

    svc = request.find_service(name="user_rename")
    try:
        svc.rename(user, new_username)

    except (UserRenameError, ValueError) as exc:
        request.session.flash(str(exc), "error")

        return httpexceptions.HTTPFound(
            location=request.route_path(
                "admin.users",
                _query=(("username", old_username), ("authority", user.authority)),
            )
        )

    request.session.flash(
        f'The user "{old_username}" will be renamed to "{new_username}" in the '
        "background. Refresh this page to see if it's already done"
        "success",
    )

    return httpexceptions.HTTPFound(
        location=request.route_path(
            "admin.users",
            _query=(("username", new_username), ("authority", user.authority)),
        )
    )


@view_config(
    route_name="admin.users_delete",
    request_method="POST",
    permission=Permission.AdminPage.LOW_RISK,
    require_csrf=True,
)
def users_delete(request):
    user = _form_request_user(request)
    svc = request.find_service(name="user_delete")

    svc.delete_user(user)
    request.session.flash(
        f"Successfully deleted user {user.username} with authority {user.authority}"
        "success",
    )

    return httpexceptions.HTTPFound(location=request.route_path("admin.users"))


@view_config(context=UserNotFoundError)
def user_not_found(exc, request):
    request.session.flash(Markup(_(str(exc))), "error")
    return httpexceptions.HTTPFound(location=request.route_path("admin.users"))


def _form_request_user(request):
    """Return the User which a user admin form action relates to."""
    userid = request.params["userid"].strip()
    user_service = request.find_service(name="user")
    user = user_service.fetch(userid)

    if user is None:
        raise UserNotFoundError(f"Could not find user with userid {userid}")

    return user
