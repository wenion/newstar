import colander

import h.i18n
from h.schemas.base import CSRFSchema
from deform.widget import SelectWidget

_ = h.i18n.TranslationString

# TODO validator

@colander.deferred
def level_age_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs["age"])

class LevelSchema(CSRFSchema):
    name = colander.SchemaNode(colander.String(), title=_("Name"))

    abbreviation = colander.SchemaNode(colander.String(), title=_("Abbreviation"))
    start_age = colander.SchemaNode(
        colander.String(),
        title=_("From"),
        widget=level_age_select_widget,)
    end_age = colander.SchemaNode(
        colander.String(),
        title=_("To"),
        widget=level_age_select_widget,)
