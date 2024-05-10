from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound, HTTPConflict
from pyramid.view import view_config, view_defaults
from sqlalchemy import func, case, cast, String, or_

from h import form, i18n, models, paginator
from h.models.course import Course
from h.models.location import Location
from h.models.profile import Profile
from h.models.registration import RegistrationTermOption, RegistrationSourceOption, Registration
from h.schemas.forms.admin.profile import ProfileSchema
from h.security import Permission
from h.services.user_unique import DuplicateUserError


_ = i18n.TranslationString


@view_config(
    route_name="admin.profiles",
    request_method="GET",
    renderer="h:templates/admin/profiles.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def profile_index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(or_(func.lower(Profile.last_name).like(f"%{q_param.lower()}%"),
                                func.lower(Profile.first_name).like(f"%{q_param.lower()}%"),
                                func.lower(Profile.number).like(f"%{q_param.lower()}%"),
                                ))

    return (
        request.db.query(Profile)
        .filter(*filter_terms)
        .order_by(Profile.created.asc())
    )


@view_defaults(
    route_name="admin.profiles_create",
    renderer="h:templates/admin/profiles_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class ProfileCreateController:
    def __init__(self, request):
        registration_list = request.find_service(name='registration').get_list()
        profile_list = request.find_service(name='profile').get_list()
        user_list = request.find_service(name="user").get_list()
        self.schema = ProfileSchema().bind(request=request, registration=registration_list, profile=profile_list, user=user_list)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create registration"),)
        )

    @view_config(request_method="GET")
    def get(self):
        # self.form.set_appstruct({"authority": self.request.default_authority})
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            number= appstruct["number"]
            last_name = appstruct["last_name"]
            first_name = appstruct["first_name"]
            date_of_birth = appstruct["date_of_birth"]
            gender = appstruct["gender"]
            phone = appstruct["phone"]
            wechat = appstruct["wechat"]
            email = appstruct["email"]
            first_emergency_contact = appstruct["first_emergency_contact"]
            second_emergency_contact = appstruct["second_emergency_contact"]
            emergency_contact = appstruct["emergency_contact"]
            memeo = appstruct["memeo"]

            registration_id = appstruct["registration"]
            referer_id = appstruct["referer"]
            user_id = appstruct["user"]

            try:
                self.request.find_service(name='profile').ensure_unique(number)
            except DuplicateUserError as err:
                raise HTTPConflict(str(err)) from err

            opt = Profile(
                number=number,
                last_name=last_name,
                first_name=first_name,
                date_of_birth=date_of_birth,
                gender=gender,
                wechat=wechat,
                phone=phone,
                email=email,
                first_emergency_contact=first_emergency_contact,
                second_emergency_contact=second_emergency_contact,
                emergency_contact=emergency_contact,
                registration_id=registration_id,
                referer_id=referer_id,
                user_id=user_id,
                memeo=memeo,
                )

            self.request.db.add(opt)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new profile {}".format(last_name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.profiles"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.profiles_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/profiles_edit.html.jinja2",
)
class ProfileEditController:
    def __init__(self, context, request):
        registration_list = request.find_service(name='registration').get_list()
        profile_list = request.find_service(name='profile').get_list()
        user_list = request.find_service(name="user").get_list()

        self.opt = context.profile
        self.request = request
        self.schema = ProfileSchema().bind(
            request=request,
            registration=registration_list,
            profile=profile_list,
            user=user_list
            )
        self.form = request.create_form(self.schema, buttons=(_("Save"),), return_url=self.request.route_url("admin.profiles"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.profiles_delete")
    def delete(self):
        # TODO Prevent deletion while the organization has associated groups.
        # group_count = (
        #     self.request.db.query(models.Group)
        #     .filter_by(organization=self.organization)
        #     .count()
        # )
        # if group_count > 0:
        #     self.request.response.status_int = 400
        #     self.request.session.flash(
        #         _(
        #             # pylint:disable=consider-using-f-string
        #             "Cannot delete organization because it is associated with {} groups".format(
        #                 group_count
        #             )
        #         ),
        #         "error",
        #     )
        #     return self._template_context()

        # Delete the organization.
        self.request.db.delete(self.opt)
        self.request.session.flash(
            _(
                # pylint:disable=consider-using-f-string
                "Successfully deleted profile %s" % (self.opt.number),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.profiles"))

    @view_config(request_method="POST")
    def update(self):
        org = self.opt

        def on_success(appstruct):
            if org.number != appstruct["number"]:
                try:
                    self.request.find_service(name='profile').ensure_unique(appstruct["number"])
                except DuplicateUserError as err:
                    raise HTTPConflict(str(err)) from err

            org.number = appstruct["number"]
            org.last_name = appstruct["last_name"]
            org.first_name = appstruct["first_name"]
            org.date_of_birth = appstruct["date_of_birth"]
            org.gender = appstruct["gender"]
            org.phone = appstruct["phone"]
            org.wechat = appstruct["wechat"]
            org.email = appstruct["email"]
            org.first_emergency_contact = appstruct["first_emergency_contact"]
            org.second_emergency_contact = appstruct["second_emergency_contact"]
            org.emergency_contact = appstruct["emergency_contact"]
            org.memeo = appstruct["memeo"]
            org.registration_id = appstruct["registration"]
            org.referer_id = appstruct["referer"]
            org.user_id = appstruct["user"]

            self._update_appstruct()

            return self._template_context()

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _update_appstruct(self):
        org = self.opt
        self.form.set_appstruct({
            "number": org.number,
            "last_name": org.last_name,
            "first_name": org.first_name,
            "date_of_birth": org.date_of_birth,
            "gender": org.gender,
            "phone": org.phone,
            "wechat": org.wechat,
            "email": org.email,
            "first_emergency_contact": org.first_emergency_contact,
            "second_emergency_contact": org.second_emergency_contact,
            "emergency_contact": org.emergency_contact,
            "memeo": org.memeo,

            "registration": org.registration_id,
            "referer": org.referer_id,
            "user": org.user_id,
        })

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.profiles_delete", id=self.opt.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
