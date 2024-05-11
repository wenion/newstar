from markupsafe import Markup
from pyramid.httpexceptions import HTTPFound, HTTPConflict
from pyramid.view import view_config, view_defaults
from sqlalchemy import func, or_

from h import form, i18n, models, paginator
from h.models.item import CostItem
from h.schemas.forms.admin.item import CostItemCreateSchema, CostItemEditSchema
from h.security import Permission
from h.services.user_unique import DuplicateUserError


_ = i18n.TranslationString


@view_config(
    route_name="admin.cost_items",
    request_method="GET",
    renderer="h:templates/admin/cost_items.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
@paginator.paginate_query
def cost_item_index(_context, request):
    q_param = request.params.get("q")

    filter_terms = []
    if q_param:
        filter_terms.append(or_(func.lower(CostItem.name).like(f"%{q_param.lower()}%"),
                                func.lower(CostItem.number).like(f"%{q_param.lower()}%"),
                                ))

    return (
        request.db.query(CostItem)
        .filter(*filter_terms)
        .order_by(CostItem.number.asc())
    )


@view_defaults(
    route_name="admin.cost_items_create",
    renderer="h:templates/admin/cost_items_create.html.jinja2",
    permission=Permission.AdminPage.LOW_RISK,
)
class ProfileCreateController:
    def __init__(self, request):
        level_list = request.find_service(name="level").get_list()
        term_list = request.find_service(name="term").get_list()
        self.schema = CostItemCreateSchema().bind(request=request, level=level_list, term=term_list)
        self.request = request
        self.form = request.create_form(
            self.schema, buttons=(_("Create cost item"),)
        )

    @view_config(request_method="GET")
    def get(self):
        # self.form.set_appstruct({"authority": self.request.default_authority})
        return self._template_context()

    @view_config(request_method="POST")
    def post(self):
        def on_success(appstruct):
            number= appstruct["number"]
            name = appstruct["name"]
            price = float(appstruct["price"])
            comments = appstruct["comments"]
            level_id = appstruct["level"]
            term_id = appstruct["term"]

            gst_included = round(price / 11, 2)

            try:
                self.request.find_service(name='cost_item').ensure_unique(number)
            except DuplicateUserError as err:
                raise HTTPConflict(str(err)) from err

            opt = CostItem(
                number=number,
                name=name,
                price=price,
                gst_included=gst_included,
                comments=comments,
                level_id=level_id,
                term_id=term_id
                )

            self.request.db.add(opt)
            self.request.session.flash(
                # pylint:disable=consider-using-f-string
                Markup(_("Created new item {}".format(number))),
                "success",
            )

            return HTTPFound(location=self.request.route_url("admin.cost_items"))

        return form.handle_form_submission(
            self.request,
            self.form,
            on_success=on_success,
            on_failure=self._template_context,
        )

    def _template_context(self):
        return {"form": self.form.render()}


@view_defaults(
    route_name="admin.cost_items_edit",
    permission=Permission.AdminPage.LOW_RISK,
    renderer="h:templates/admin/cost_items_edit.html.jinja2",
)
class CostItemEditController:
    def __init__(self, context, request):
        level_list = request.find_service(name="level").get_list()
        term_list = request.find_service(name="term").get_list()
        
        self.opt = context.cost_item
        self.request = request
        self.schema = CostItemEditSchema().bind(
            request=request,
            level=level_list,
            term=term_list
            )
        self.form = request.create_form(self.schema, buttons=(_("Save"),), return_url=self.request.route_url("admin.cost_items"))
        self._update_appstruct()

    @view_config(request_method="GET")
    def read(self):
        return self._template_context()

    @view_config(request_method="POST", route_name="admin.cost_items_delete")
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
        return HTTPFound(location=self.request.route_path("admin.cost_items"))

    @view_config(request_method="POST")
    def update(self):
        org = self.opt

        def on_success(appstruct):
            if org.number != appstruct["number"]:
                try:
                    self.request.find_service(name='cost_item').ensure_unique(appstruct["number"])
                except DuplicateUserError as err:
                    raise HTTPConflict(str(err)) from err

            org.number = appstruct["number"]
            org.name = appstruct["name"]
            org.price = appstruct["price"]
            org.gst_included = appstruct["gst_included"]
            org.comments = appstruct["comments"]
            org.level_id = appstruct["level"]
            org.term_id = appstruct["term"]

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
            "name": org.name,
            "price": org.price,
            "gst_included": org.gst_included,
            "comments": org.comments,
            "level": org.level_id,
            "term": org.term_id,
        })

    def _template_context(self):
        delete_url = self.request.route_url(
            "admin.cost_items_delete", id=self.opt.id
        )
        return {"form": self.form.render(), "delete_url": delete_url}
