from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func, case, cast, String, or_

from h import form, i18n, models, paginator
from h.models.course import Course
from h.models.location import Location
from h.models.registration import RegistrationTermOption, RegistrationSourceOption, Registration
from h.schemas.forms.admin.registration import RegistrationOptionSchema, RegistrationSchema
from h.security import Permission

_ = i18n.TranslationString

day_replacements = {
    'MON': 'Monday',
    'TUE': 'Tuesday',
    'WED': 'Wednesday',
    'THU': 'Thursday',
    'FRI': 'Friday',
    'SAT': 'Saturday',
    'SUN': 'Sunday',
}

day_order = {
    'MON': 1,
    'TUE': 2,
    'WED': 3,
    'THU': 4,
    'FRI': 5,
    'SAT': 6,
    'SUN': 7,
}

def get_course_options(request):
    case_replacement_statement = case(day_replacements, value=Course.day, else_='')
    case_order_statement = case(day_order, value=Course.day,else_=0)
    combined_name_day = func.concat(Location.name, ' - ', case_replacement_statement, ' - ', Course.time)

    return request.db.query(cast(func.min(Course.id), String), combined_name_day) \
        .join(Location, Location.id == Course.location_id) \
        .group_by(Location.name, Course.day, Course.time) \
        .order_by(Location.name.asc(), case_order_statement).all()


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


@view_config(
    route_name="admin.registrations",
    request_method="GET",
    renderer="h:templates/admin/registrations.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def registration_index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(or_(func.lower(Registration.last_name).like(f"%{q_param.lower()}%"),
                                func.lower(Registration.first_name).like(f"%{q_param.lower()}%")))

    return (
        request.db.query(Registration)
        .filter(*filter_terms)
        .order_by(Registration.created.asc())
    )


@view_defaults(
    route_name="admin.registrations_create",
    renderer="h:templates/admin/registrations_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class RegistrationCreateController:
    def __init__(self, request):
        level_list = [(str(item.id), item.name) for item in request.find_service(name='level').get_all()]
        term_list = [(str(item.id), item.name) for item in request.find_service(name='registration_term_option').get_all()]
        source_list = [(str(item.id), item.name) for item in request.find_service(name='registration_source_option').get_all()]

        self.schema = RegistrationSchema().bind(request=request, code=get_course_options(request), level=level_list, term=term_list, source=source_list)
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
            last_name = appstruct["last_name"]
            first_name = appstruct["first_name"]
            date_of_birth = appstruct["date_of_birth"]
            gender = appstruct["gender"]
            wechat = appstruct["wechat"]
            email = appstruct["email"]
            first_emergency_contact = appstruct["first_emergency_contact"]
            second_emergency_contact = appstruct["second_emergency_contact"]
            emergency_contact = appstruct["emergency_contact"]
            level_id = appstruct["level"]
            code_id = appstruct["code"]
            term_id = appstruct["term"]
            source_id = appstruct["source"]
            referer = appstruct["referer"]
            memeo = appstruct["memeo"]

            course = self.request.find_service(name='course').get_by_id(code_id)
            location_id = course.location_id

            opt = Registration(
                last_name=last_name,
                first_name=first_name,
                date_of_birth=date_of_birth,
                gender=gender,
                wechat=wechat,
                email=email,
                first_emergency_contact=first_emergency_contact,
                second_emergency_contact=second_emergency_contact,
                emergency_contact=emergency_contact,
                level_id=level_id,
                code_id=code_id,
                term_id=term_id,
                source_id=source_id,
                location_id=location_id,
                referer=referer,
                memeo=memeo,
                )

            self.request.db.add(opt)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new registeration {}".format(last_name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.registrations"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.registrations_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/registrations_edit.html.jinja2",
)
class RegistrationEditController:
    def __init__(self, context, request):
        level_list = [(str(item.id), item.name) for item in request.find_service(name='level').get_all()]
        term_list = [(str(item.id), item.name) for item in request.find_service(name='registration_term_option').get_all()]
        source_list = [(str(item.id), item.name) for item in request.find_service(name='registration_source_option').get_all()]

        self.opt = context.registration
        self.request = request
        self.schema = RegistrationSchema().bind(request=request, code=get_course_options(request), level=level_list, term=term_list, source=source_list)
        self.form = request.create_form(self.schema, buttons=(_("Save"),), return_url=self.request.route_url("admin.registrations"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.registrations_delete")
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
                "Successfully deleted registeration %s" % (self.opt.last_name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.registrations"))

    @view_config(request_method="POST")
    def update(self):
        org = self.opt

        def on_success(appstruct):
            org.last_name = appstruct["last_name"]
            org.first_name = appstruct["first_name"]
            org.date_of_birth = appstruct["date_of_birth"]
            org.gender = appstruct["gender"]
            org.wechat = appstruct["wechat"]
            org.email = appstruct["email"]
            org.first_emergency_contact = appstruct["first_emergency_contact"]
            org.second_emergency_contact = appstruct["second_emergency_contact"]
            org.emergency_contact = appstruct["emergency_contact"]
            org.level_id = appstruct["level"]
            org.code_id = appstruct["code"]
            org.term_id = appstruct["term"]
            org.source_id = appstruct["source"]
            org.referer = appstruct["referer"]
            org.memeo = appstruct["memeo"]

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
            "last_name": org.last_name,
            "first_name": org.first_name,
            "date_of_birth": org.date_of_birth,
            "gender": org.gender,
            "wechat": org.wechat,
            "email": org.email,
            "first_emergency_contact": org.first_emergency_contact,
            "second_emergency_contact": org.second_emergency_contact,
            "emergency_contact": org.emergency_contact,
            "level": org.level_id,
            "code": org.code_id,
            "term": org.term_id,
            "source": org.source_id,
            "referer": org.referer,
            "memeo": org.memeo,
        })

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.registrations_delete", id=self.opt.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
