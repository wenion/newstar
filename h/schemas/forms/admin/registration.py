import colander

import h.i18n
from h.schemas.base import CSRFSchema

_ = h.i18n.TranslationString

# TODO validator

class RegistrationOptionSchema(CSRFSchema):
    name = colander.SchemaNode(colander.String(), title=_("Name"))

    chinese = colander.SchemaNode(colander.String(), title=_("Chinese"))
