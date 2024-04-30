import colander
import datetime

import h.i18n
from h.schemas.base import CSRFSchema
from deform.widget import TextInputWidget, SelectWidget
from h.schemas.forms.widgets import DateInputWidget

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def deferred_date_validator(node, kw):
    max_date = kw.get("max_date", datetime.date.today())
    return colander.Range(min=datetime.date.min, max=max_date)

@colander.deferred
def deferred_date_description(node, kw):
    max_date = kw.get("max_date", datetime.date.today())
    return "Date (no earlier than %s)" % max_date.ctime()

@colander.deferred
def term_number_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs["number"])

class TermSchema(CSRFSchema):
    name = colander.SchemaNode(
        colander.String(),
        title=_("Name"),
        default="Term",
        widget=TextInputWidget()
    )

    number = colander.SchemaNode(
        colander.Int(),
        title=_("Term"),
        default=1,
        widget=term_number_select_widget,)
    
    year = colander.SchemaNode(
        colander.Int(),
        title=_("Year"),
        default=datetime.datetime.now().year,
        widget=TextInputWidget(mask="9999")
    )

    start_date = colander.SchemaNode(
        colander.Date(),
        title=_("Start Date"),
        widget=DateInputWidget(),
        )

    end_date = colander.SchemaNode(
        colander.Date(),
        title=_("End Date"),
        # default=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        widget=DateInputWidget(),)
    
    number_of_weeks = colander.SchemaNode(
        colander.Int(),
        title=_("Number of weeks"),
        default=10,
        widget=TextInputWidget(mask="9")
    )
