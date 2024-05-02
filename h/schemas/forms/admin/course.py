import colander
import datetime
from deform.widget import TextInputWidget, SelectWidget

import h.i18n
from h.schemas.base import CSRFSchema

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def course_location_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs["location"])

@colander.deferred
def course_day_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs["day"])

@colander.deferred
def course_level_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs["level"])

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
        colander.Int(),
        title=_("Location"),
        widget=course_location_select_widget,
    )

    day = colander.SchemaNode(
        colander.String(),
        title=_("Day"),
        widget=course_day_select_widget,
    )

    time = colander.SchemaNode(
        colander.String(),
        title=_("Time"),
        validator=time_validator,
        widget=TextInputWidget()
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

    time = colander.SchemaNode(
        colander.String(),
        title=_("Time"),
        validator=time_validator,
        widget=TextInputWidget()
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