from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from sqlalchemy import func

from h import form, i18n, models, paginator
from h.models.term import Term
from h.schemas.forms.admin.term import TermSchema
from h.security import Permission

_ = i18n.TranslationString


number = [('1', 1),
          ('2', 2),
          ('3', 3),
          ('4', 4),
          ('5', 5),
          ('6', 6),]


def calculate_weeks(start_date, end_date):
    delta = end_date - start_date

    # Calculate the number of weeks (rounding up to the nearest week)
    weeks = (delta.days + 6) // 7  # Adding 6 to ensure rounding up

    return weeks


@view_config(
    route_name="admin.terms",
    request_method="GET",
    renderer="h:templates/admin/terms.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(Term.year==int(q_param))

    return (
        request.db.query(Term)
        .filter(*filter_terms)
        .order_by(Term.number.asc(), Term.start_date.asc())
    )


@view_defaults(
    route_name="admin.terms_create",
    renderer="h:templates/admin/terms_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class TermCreateController:
    def __init__(self, request):
        self.schema = TermSchema().bind(request=request, number=number)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create term"),)
        )

    @view_config(request_method="GET")
    def get(self):
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            name = appstruct["name"]
            number = appstruct["number"]
            year = appstruct["year"]
            start_date = appstruct["start_date"]
            end_date = appstruct["end_date"]
            number_of_weeks = calculate_weeks(start_date, end_date)
            term = Term(name=name, number=number, year=year, start_date=start_date, end_date=end_date, number_of_weeks=number_of_weeks)

            self.request.db.add(term)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new term {}".format(name + " "+ str(number)))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.terms"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.terms_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/terms_edit.html.jinja2",
)
class TermEditController:
    def __init__(self, context, request):
        self.term = context.term
        self.request = request
        self.schema = TermSchema().bind(request=request, number=number)
        self.form = request.create_form(
            self.schema, buttons=(_("Save"),),
            return_url=self.request.route_url("admin.terms"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.terms_delete")
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
        self.request.db.delete(self.term)
        self.request.session.flash(
            _(
                # pylint:disable=consider-using-f-string
                "Successfully deleted term %s" % (self.term.name),
                "success",
            )
        )
        return HTTPFound(location=self.request.route_path("admin.terms"))

    @view_config(request_method="POST")
    def update(self):
        org = self.term

        def on_success(appstruct):
            org.name = appstruct["name"]
            org.number = appstruct["number"]
            org.year = appstruct["year"]
            org.start_date = appstruct["start_date"]
            org.end_date = appstruct["end_date"]
            org.number_of_weeks = appstruct["number_of_weeks"]

            self._update_appstruct()

            return self._template_context()

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _update_appstruct(self):
        org = self.term
        self.form.set_appstruct(
            {"name": org.name, "number": org.number, "year": org.year, "start_date": org.start_date, "end_date": org.end_date, "number_of_weeks": org.number_of_weeks}
        )

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.terms_delete", id=self.term.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
