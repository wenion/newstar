import colander
from deform.widget import TextInputWidget, SelectWidget, OptGroup

import h.i18n
from h.schemas.base import CSRFSchema
from h.schemas.forms.widgets import TimeInputWidget, DateTimeInputWidget


_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def plan_course_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select Course --'),] + kwargs['code'])

@colander.deferred
def plan_term_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select term --'),] + kwargs["term"])

@colander.deferred
def plan_location_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select location --'),] + kwargs["location"])

@colander.deferred
def plan_level_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select level --'),] + kwargs["level"])


class PlanSchema(CSRFSchema):
    name = colander.SchemaNode(
        colander.String(),
        title=_("Display Name"),
        widget=TextInputWidget(),
    )

    code_id = colander.SchemaNode(
        colander.String(),
        title=_("Class Code"),
        widget=plan_course_select_widget,
    )

    term_id = colander.SchemaNode(
        colander.String(),
        title=_("Term"),
        widget=plan_term_select_widget,
    )

    location_id = colander.SchemaNode(
        colander.String(),
        title=_("Location"),
        widget=plan_location_select_widget,
    )

    level_id = colander.SchemaNode(
        colander.String(),
        title=_("Level"),
        widget=plan_level_select_widget,
    )

    start_time = colander.SchemaNode(
        colander.String(),
        title=_("To"),
        widget=TimeInputWidget(),
    )

    end_time = colander.SchemaNode(
        colander.String(),
        title=_("From"),
        widget=TimeInputWidget()
    )

    memeo = colander.SchemaNode(
        colander.String(),
        title=_("Memeo"),
        widget=TextInputWidget(),
        missing=""
    )


class PlanEditSchema(CSRFSchema):
    name = colander.SchemaNode(
        colander.String(),
        title=_("Display Name"),
        widget=TextInputWidget(),
    )

    code_id = colander.SchemaNode(
        colander.String(),
        title=_("Class Code"),
        widget=plan_course_select_widget,
    )

    term_id = colander.SchemaNode(
        colander.String(),
        title=_("Term"),
        widget=plan_term_select_widget,
    )

    location_id = colander.SchemaNode(
        colander.String(),
        title=_("Location"),
        widget=plan_location_select_widget,
    )

    level_id = colander.SchemaNode(
        colander.String(),
        title=_("Level"),
        widget=plan_level_select_widget,
    )

    start_time = colander.SchemaNode(
        colander.DateTime(),
        title=_("To"),
        widget=DateTimeInputWidget(),
    )

    end_time = colander.SchemaNode(
        colander.DateTime(),
        title=_("From"),
        widget=DateTimeInputWidget()
    )

    memeo = colander.SchemaNode(
        colander.String(),
        title=_("Memeo"),
        widget=TextInputWidget(),
        missing=""
    )
