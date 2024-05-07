from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func

from h import form, i18n, models, paginator
from h.models.registration import RegistrationTermOption,  RegistrationSourceOption
from h.schemas.forms.admin.registration import RegistrationOptionSchema
from h.security import Permission

_ = i18n.TranslationString


@view_config(
    route_name="admin.registration_term_options",
    request_method="GET",
    renderer="h:templates/admin/registration_term_options.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def registration_term_options_index(_context, request):
    return (
        request.db.query(RegistrationTermOption)
        .order_by(RegistrationTermOption.created.asc())
    )


@view_defaults(
    route_name="admin.registration_term_options_create",
    renderer="h:templates/admin/registration_term_options_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class RegistrationTermOptionCreateController:
    def __init__(self, request):
        self.schema = RegistrationOptionSchema().bind(request=request)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create registration term option"),)
        )

    @view_config(request_method="GET")
    def get(self):
        # self.form.set_appstruct({"authority": self.request.default_authority})
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            name = appstruct["name"]
            chinese = appstruct["chinese"]
            opt = RegistrationTermOption(name=name, chinese=chinese)

            self.request.db.add(opt)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new option {}".format(name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.registration_term_options"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.registration_term_options_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/registration_term_options_edit.html.jinja2",
)
class RegistrationTermOptionEditController:
    def __init__(self, context, request):
        self.opt = context.opt
        self.request = request
        self.schema = RegistrationOptionSchema().bind(request=request)
        self.form = request.create_form(self.schema, buttons=(_("Save"),), return_url=self.request.route_url("admin.registration_term_options"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.registration_term_options_delete")
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
                "Successfully deleted option %s" % (self.opt.name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.registration_term_options"))

    @view_config(request_method="POST")
    def update(self):
        org = self.opt

        def on_success(appstruct):
            org.name = appstruct["name"]
            org.chinese = appstruct["chinese"]

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
        self.form.set_appstruct(
            {"name": org.name, "chinese": org.chinese}
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.registration_term_options_delete", id=self.opt.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}



@view_config(
    route_name="admin.registration_source_options",
    request_method="GET",
    renderer="h:templates/admin/registration_source_options.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def registration_source_options_index(_context, request):
    return (
        request.db.query(RegistrationSourceOption)
        .order_by(RegistrationSourceOption.created.asc())
    )


@view_defaults(
    route_name="admin.registration_source_options_create",
    renderer="h:templates/admin/registration_source_options_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class RegistrationSourceOptionCreateController:
    def __init__(self, request):
        self.schema = RegistrationOptionSchema().bind(request=request)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create registration source option"),)
        )

    @view_config(request_method="GET")
    def get(self):
        # self.form.set_appstruct({"authority": self.request.default_authority})
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            name = appstruct["name"]
            chinese = appstruct["chinese"]
            opt = RegistrationSourceOption(name=name, chinese=chinese)

            self.request.db.add(opt)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new option {}".format(name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.registration_source_options"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.registration_source_options_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/registration_source_options_edit.html.jinja2",
)
class RegistrationSourceOptionEditController:
    def __init__(self, context, request):
        self.opt = context.opt
        self.request = request
        self.schema = RegistrationOptionSchema().bind(request=request)
        self.form = request.create_form(self.schema, buttons=(_("Save"),), return_url=self.request.route_url("admin.registration_source_options"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.registration_source_options_delete")
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
                "Successfully deleted option %s" % (self.opt.name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.registration_source_options"))

    @view_config(request_method="POST")
    def update(self):
        org = self.opt

        def on_success(appstruct):
            org.name = appstruct["name"]
            org.chinese = appstruct["chinese"]

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
        self.form.set_appstruct(
            {"name": org.name, "chinese": org.chinese}
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.registration_source_options_delete", id=self.opt.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
