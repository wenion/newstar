from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func

from h import form, i18n, models, paginator
from h.models.location import Location
from h.schemas.forms.admin.location import LocationSchema
from h.security import Permission

_ = i18n.TranslationString


@view_config(
    route_name="admin.locations",
    request_method="GET",
    renderer="h:templates/admin/locations.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(func.lower(Location.abbreviation).like(f"%{q_param.lower()}%"))

    return (
        request.db.query(Location)
        .filter(*filter_terms)
        .order_by(Location.created.asc())
    )


@view_defaults(
    route_name="admin.locations_create",
    renderer="h:templates/admin/locations_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class LocationCreateController:
    def __init__(self, request):
        self.schema = LocationSchema().bind(request=request)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create location"),)
        )

    @view_config(request_method="GET")
    def get(self):
        # self.form.set_appstruct({"authority": self.request.default_authority})
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            name = appstruct["name"]
            abbreviation = appstruct["abbreviation"]
            address = appstruct["address"]
            location = Location(name=name, abbreviation=abbreviation, address=address)

            self.request.db.add(location)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new location {}".format(name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.locations"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.locations_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/locations_edit.html.jinja2",
)
class LocationEditController:
    def __init__(self, context, request):
        self.location = context.location
        self.request = request
        self.schema = LocationSchema().bind(request=request)
        self.form = request.create_form(self.schema, buttons=(_("Save"),), return_url=self.request.route_url("admin.locations"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.locations_delete")
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
        self.request.db.delete(self.location)
        self.request.session.flash(
            _(
                # pylint:disable=consider-using-f-string
                "Successfully deleted location %s" % (self.location.name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.locations"))

    @view_config(request_method="POST")
    def update(self):
        org = self.location

        def on_success(appstruct):
            org.name = appstruct["name"]
            org.abbreviation = appstruct["abbreviation"]
            org.address = appstruct["address"]

            self._update_appstruct()

            return self._template_context()

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _update_appstruct(self):
        org = self.location
        self.form.set_appstruct(
            {"name": org.name, "abbreviation": org.abbreviation, "address": org.address}
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.locations_delete", id=self.location.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
