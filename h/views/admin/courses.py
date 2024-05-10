from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func, case, String

from h import form, i18n, models, paginator
from h.models.course import Course
from h.models.level import Level
from h.models.location import Location
from h.models.plan import Plan
from h.schemas.forms.admin.course import CourseSchema, CourseEditSchema
from h.security import Permission

_ = i18n.TranslationString

day = [('MON', 'MON'),
       ('TUE', 'TUE'),
       ('WED', 'WED'),
       ('THU', 'THU'),
       ('FRI', 'FRI'),
       ('SAT', 'SAT'),
       ('SUN', 'SUN'),]

day_order = {
    'MON': 1,
    'TUE': 2,
    'WED': 3,
    'THU': 4,
    'FRI': 5,
    'SAT': 6,
    'SUN': 7,
}
case_statement = case(day_order, value=Course.day,else_=0)


@view_config(
    route_name="admin.courses",
    request_method="GET",
    renderer="h:templates/admin/courses.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(func.lower(Course.code).like(f"%{q_param.lower()}%"))

    return (
        request.db.query(Course.id,
                         Course.year,
                         Location.name,
                         Course.day,
                         Course.start_time,
                         Course.end_time,
                         Level.name,
                         Course.code,
                         Course.memeo,
                         func.string_agg(Plan.id.cast(String), ', ').label('plan_ids'),
                         func.string_agg(Plan.name, ', ').label('plan_names')
                         )
        .filter(*filter_terms)
        .outerjoin(Plan, Plan.code_id == Course.id)
        .outerjoin(Location, Location.id == Course.location_id)
        .outerjoin(Level, Level.id == Course.level_id)
        .group_by(Course.id, Course.year, Location.name, Course.day, Course.start_time, Course.end_time, Level.name, Course.code, Course.memeo)
        .order_by(Course.year.asc(), Course.location_id.asc(), Course.level_id.asc(), case_statement, Course.start_time.asc(), Course.code.asc())
    )


@view_defaults(
    route_name="admin.courses_create",
    renderer="h:templates/admin/courses_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class CourseCreateController:
    def __init__(self, request):
        location_list = [(item.id, item.name) for item in request.find_service(name='location').get_all()]
        level_list = [(item.id, item.name) for item in request.find_service(name='level').get_all()]

        self.schema = CourseSchema().bind(request=request, location=location_list, level=level_list, day=day)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create course"),)
        )

    @view_config(request_method="GET")
    def get(self):
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            year = appstruct["year"]
            location_id = appstruct["location_id"]
            day = appstruct["day"]
            start_time = appstruct["start_time"]
            end_time = appstruct["end_time"]
            level_id = appstruct["level_id"]
            memeo = appstruct["memeo"]

            location = self.request.find_service(name="location").get_by_id(location_id)
            level = self.request.find_service(name="level").get_by_id(level_id)
            code = location.abbreviation + day + start_time.strftime('%H%M') + level.abbreviation

            course = Course(year=year, location=location, day=day, start_time=start_time, end_time=end_time, level=level, code=code, memeo=memeo)

            self.request.db.add(course)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new course {}".format(code))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.courses"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.courses_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/courses_edit.html.jinja2",
)
class CourseEditController:
    def __init__(self, context, request):
        location_list = [(str(item.id), item.name) for item in request.find_service(name='location').get_all()]
        level_list = [(str(item.id), item.name) for item in request.find_service(name='level').get_all()]

        self.course = context.course
        self.request = request
        self.schema = CourseEditSchema().bind(request=request, location=location_list, level=level_list, day=day)
        self.form = request.create_form(
            self.schema, buttons=(_("Save"),),
            return_url=self.request.route_url("admin.courses"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.courses_delete")
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

        # Delete the term.
        self.request.db.delete(self.course)
        self.request.session.flash(
            _(
                # pylint:disable=consider-using-f-string
                "Successfully deleted course %s" % (self.course.code),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.courses"))

    @view_config(request_method="POST")
    def update(self):
        org = self.course

        def on_success(appstruct):
            org.year = appstruct["year"]
            org.location_id = appstruct["location_id"]
            org.day = appstruct["day"]
            org.start_time = appstruct["start_time"]
            org.end_time = appstruct["end_time"]
            org.level_id = appstruct["level_id"]
            org.code = appstruct["code"]
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
        org = self.course
        self.form.set_appstruct(
            {
                "year": org.year,
                "location_id": org.location_id,
                "day": org.day,
                "start_time": org.start_time,
                "end_time": org.end_time,
                "level_id": org.level_id,
                "code": org.code,
                "memeo": org.memeo,
            }
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.courses_delete", id=self.course.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
