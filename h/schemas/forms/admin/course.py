import colander
import datetime
from deform.widget import TextInputWidget, SelectWidget

import h.i18n
from h.schemas.base import CSRFSchema
from h.schemas.forms.widgets import TimeInputWidget

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def course_location_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select location --'),] + kwargs["location"])

@colander.deferred
def course_day_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs["day"])

@colander.deferred
def course_level_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select level --'),] + kwargs["level"])

def time_validator(node, value):
    try:
        datetime.datetime.strptime(value, "%H%M")
    except:
        raise colander.Invalid(node, _("Invalid time format. Please enter time in format 'hhmm' (e.g., 1330)."))

class CourseSchema(CSRFSchema):
    year = colander.SchemaNode(
        colander.Int(),
        title=_("Year"),
        default=datetime.datetime.now().year,
        widget=TextInputWidget(mask="9999")
    )

    location_id = colander.SchemaNode(
        colander.String(),
        title=_("Location"),
        widget=course_location_select_widget,
    )

    day = colander.SchemaNode(
        colander.String(),
        title=_("Day"),
        widget=course_day_select_widget,
    )

    start_time = colander.SchemaNode(
        colander.Time(),
        title=_("Time From"),
        widget=TimeInputWidget()
    )

    end_time = colander.SchemaNode(
        colander.Time(),
        title=_("Time To"),
        widget=TimeInputWidget()
    )

    level_id = colander.SchemaNode(
        colander.String(),
        title=_("Level"),
        widget=course_level_select_widget,
    )

    memeo = colander.SchemaNode(
        colander.String(),
        title=_("Memeo"),
        widget=TextInputWidget(),
        missing=""
    )


class CourseEditSchema(CSRFSchema):
    year = colander.SchemaNode(
        colander.Int(),
        title=_("Year"),
        default=datetime.datetime.now().year,
        widget=TextInputWidget(mask="9999")
    )

    code = colander.SchemaNode(
        colander.String(),
        title=_("Code"),
        widget=TextInputWidget()
    )

    location_id = colander.SchemaNode(
        colander.Int(),
        title=_("Location"),
        widget=course_location_select_widget,
    )

    day = colander.SchemaNode(
        colander.String(),
        title=_("Day"),
        widget=course_day_select_widget,
    )

    start_time = colander.SchemaNode(
        colander.Time(),
        title=_("Time From"),
        widget=TimeInputWidget()
    )

    end_time = colander.SchemaNode(
        colander.Time(),
        title=_("Time To"),
        widget=TimeInputWidget()
    )

    level_id = colander.SchemaNode(
        colander.Int(),
        title=_("Level"),
        widget=course_level_select_widget,
    )

    memeo = colander.SchemaNode(
        colander.String(),
        title=_("Memeo"),
        widget=TextInputWidget(),
        missing=""
    )