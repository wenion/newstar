import colander

import h.i18n
from h.schemas.base import CSRFSchema

_ = h.i18n.TranslationString

# TODO validator

class LocationSchema(CSRFSchema):
    name = colander.SchemaNode(colander.String(), title=_("Name"))

    abbreviation = colander.SchemaNode(colander.String(), title=_("Abbreviation"))
    address = colander.SchemaNode(colander.String(), title=_("Address"))
