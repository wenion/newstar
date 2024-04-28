from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func

from h import form, i18n, models, paginator
from h.models.level import Level
from h.schemas.forms.admin.level import LevelSchema
from h.security import Permission

_ = i18n.TranslationString


age_list =[('4', '4'),
           ('5', '5'),
           ('6', '6'),
           ('8', '8'),
           ('9', '9'),
           ('10', '10'),
           ('11', '11'),
           ('12', '12'),
           ('13', '13'),
           ('14', '14'),
           ('15', '15'),
           ('16', '16'),
           ('Infinity', 'Infinity'),]


@view_config(
    route_name="admin.levels",
    request_method="GET",
    renderer="h:templates/admin/levels.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(func.lower(Level.abbreviation).like(f"%{q_param.lower()}%"))

    return (
        request.db.query(Level)
        .filter(*filter_terms)
        .order_by(Level.start_age.asc())
    )


@view_defaults(
    route_name="admin.levels_create",
    renderer="h:templates/admin/levels_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class LevelCreateController:
    def __init__(self, request):
        self.schema = LevelSchema().bind(request=request, age=age_list)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create level"),)
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
            start_age = appstruct["start_age"]
            end_age = appstruct["end_age"]
            level = Level(name=name, abbreviation=abbreviation, start_age=start_age, end_age=end_age)

            self.request.db.add(level)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new level {}".format(name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.levels"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.levels_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/levels_edit.html.jinja2",
)
class LevelEditController:
    def __init__(self, context, request):
        self.level = context.level
        self.request = request
        self.schema = LevelSchema().bind(request=request, age=age_list)
        self.form = request.create_form(
            self.schema, buttons=(_("Save"),),
            return_url=self.request.route_url("admin.levels"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.levels_delete")
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
        self.request.db.delete(self.level)
        self.request.session.flash(
            _(
                # pylint:disable=consider-using-f-string
                "Successfully deleted level %s" % (self.level.name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.levels"))

    @view_config(request_method="POST")
    def update(self):
        org = self.level

        def on_success(appstruct):
            org.name = appstruct["name"]
            org.abbreviation = appstruct["abbreviation"]
            org.start_age = appstruct["start_age"]
            org.end_age = appstruct["end_age"]

            self._update_appstruct()

            return self._template_context()

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _update_appstruct(self):
        org = self.level
        self.form.set_appstruct(
            {"name": org.name, "abbreviation": org.abbreviation, "start_age": org.start_age, "end_age": org.end_age}
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.levels_delete", id=self.level.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
