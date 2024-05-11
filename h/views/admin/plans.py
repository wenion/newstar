from datetime import datetime, timedelta, date
from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func, case

from h import form, i18n, models, paginator
from h.models.course import Course
from h.models.plan import Plan
from h.models.term import Term
from h.schemas.forms.admin.plan import PlanSchema, PlanEditSchema
from h.security import Permission

_ = i18n.TranslationString

day_order = {
    'MON': 1,
    'TUE': 2,
    'WED': 3,
    'THU': 4,
    'FRI': 5,
    'SAT': 6,
    'SUN': 7,
}


def generate_weekday_dates(start_date, end_date, target_weekday, start_time, end_time):
    # Convert start_date and end_date strings to datetime objects
    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()
    
    # Initialize an empty list to store the generated dates
    weekday_dates = []

    # Iterate through the range of dates from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        # Check if the current date matches the specified weekday
        if current_date.weekday() == target_weekday:
            start = datetime.combine(current_date, start_time)
            end = datetime.combine(current_date, end_time)
            weekday_dates.append((start, end))
        # Move to the next date
        current_date += timedelta(days=1)

    return weekday_dates


@view_config(
    route_name="admin.plans",
    request_method="GET",
    renderer="h:templates/admin/plans.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def index(_context, request):
    q_param = request.params.get("q")

    code_param = request.params.get("name")
    term_param = request.params.get("term")

    filter_terms = []
    if q_param:
        filter_terms.append(Plan.code_id == int(q_param))
    if code_param:
        filter_terms.append(func.lower(Plan.name).like(f"%{code_param.lower()}%"))
    if term_param:
        term = request.find_service(name="term").get_by_id(int(term_param))
        if term:
            filter_terms.append(Plan.term_id == term.number)

    return (
        request.db.query(Plan)
        .filter(*filter_terms)
        .order_by(Plan.name.asc())
    )


@view_defaults(
    route_name="admin.plans_create",
    renderer="h:templates/admin/plans_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class PlanCreateController:
    def __init__(self, request):
        location_list = request.find_service(name='location').get_list()
        course_list = request.find_service(name='course').get_list()
        year = date.today().year
        term_list = [('0', 'All Terms({})'.format(year))]
        term_list += request.find_service(name='term').get_list()
        level_list = request.find_service(name='level').get_list()

        self.year = year
        self.schema = PlanSchema().bind(request=request, code=course_list, term=term_list, location=location_list, level=level_list)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create plan"),)
        )

    @view_config(request_method="GET")
    def get(self):
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            name = appstruct["name"]
            course_id = appstruct["code_id"]
            term_id = appstruct["term_id"]
            location_id = appstruct["location_id"]
            level_id = appstruct["level_id"]
            start_time = appstruct["start_time"]
            end_time = appstruct["end_time"]
            memeo = appstruct["memeo"]

            course = self.request.find_service(name="course").get_by_id(course_id)

            term_list = [self.request.find_service(name="term").get_by_id(term_id),]
            
            if term_id == '0':
                term_list = self.request.find_service(name="term").get_by_year(self.year)

            for term in term_list:
                repeat_dates = generate_weekday_dates(term.start_date, term.end_date, day_order[course.day]-1, start_time, end_time)
                for item in repeat_dates:
                    plan = Plan(name=name, code_id=course_id, term_id=term.id, location_id=location_id, level_id=level_id, start_time=item[0], end_time=item[1], memeo=memeo)
                    self.request.db.add(plan)

            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new plan class {}".format(name))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.batch_plans_list", course_id=course_id))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.plans_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/plans_edit.html.jinja2",
)
class PlanEditController:
    def __init__(self, context, request):
        location_list = request.find_service(name='location').get_list()
        course_list = request.find_service(name='course').get_list()
        term_list = request.find_service(name='term').get_list()
        level_list = request.find_service(name='level').get_list()

        self.plan = context.plan
        self.request = request
        self.schema = PlanEditSchema().bind(request=request, code=course_list, term=term_list, location=location_list, level=level_list)
        self.form = request.create_form(
            self.schema, buttons=(_("Save"),),
            return_url=self.request.route_url("admin.plans"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.plans_delete")
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
        self.request.db.delete(self.plan)
        self.request.session.flash(
            _(
                # pylint:disable=consider-using-f-string
                "Successfully deleted course %s" % (self.plan.name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.batch_plans_list", course_id=self.plan.code_id))

    @view_config(request_method="POST")
    def update(self):
        org = self.plan

        def on_success(appstruct):
            org.name = appstruct["name"]
            org.code_id = appstruct["code_id"]
            org.term_id = appstruct["term_id"]
            org.location_id = appstruct["location_id"]
            org.level_id = appstruct["level_id"]
            org.start_time = appstruct["start_time"]
            org.end_time = appstruct["end_time"]
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
        plan = self.plan
        self.form.set_appstruct(
            {
                "name": plan.name,
                "code_id": plan.code_id,
                "term_id": plan.term_id,
                "location_id": plan.location_id,
                "level_id": plan.level_id,
                "start_time": plan.start_time,
                "end_time": plan.end_time,
                "memeo": plan.memeo,
            }
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.plans_delete", id=self.plan.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}


@view_config(
    route_name="admin.batch_plans",
    request_method="GET",
    renderer="h:templates/admin/batch_plans.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def batch_index(_context, request):
    course_code = request.params.get("q")

    filter_terms = []
    if course_code:
        filter_terms.append(func.lower(Plan.name).like(f"%{course_code.lower()}%"))

    return (
        request.db.query(Plan.code_id, Plan.name, Course.code, Course.memeo, func.count(Plan.id)) #, func.count(Term.id))
        .add_columns(func.array_agg(Course.memeo))
        .filter(*filter_terms)
        .join(Course, Plan.code_id == Course.id, isouter=True)
        # .join(Term, Plan.term_id == Term.id, isouter=True)
        .group_by(Plan.code_id, Plan.name, Course.code, Course.memeo) #, Term.number)
        .order_by(Plan.name.asc())
    )


@view_config(
    route_name="admin.batch_plans_list",
    request_method="GET",
    renderer="h:templates/admin/batch_plans_list.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def batch_detail_index(_context, request):
    course_id = request.matchdict.get("course_id")

    filter_terms = []
    if course_id:
        filter_terms.append(Plan.code_id==int(course_id))

    return (
        request.db.query(Plan.code_id, Plan.name, Course.code, Course.memeo, func.count(Plan.id), Term.number)
        .filter(*filter_terms)
        .join(Course, Plan.code_id == Course.id, isouter=True)
        .join(Term, Plan.term_id == Term.id, isouter=True)
        .group_by(Plan.code_id, Plan.name, Course.code, Course.memeo, Term.number)
        .order_by(Plan.name.asc())
    )
