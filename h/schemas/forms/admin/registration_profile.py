import colander
from deform.widget import SelectWidget

import h.i18n
from h.schemas.base import CSRFSchema

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def registration_profile_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select profile --'),] + kwargs['profile'])


class ProfileSelectSchema(CSRFSchema):
    profile = colander.SchemaNode(
        colander.String(),
        title=_("Select Profile"),
        widget=registration_profile_select_widget,
    )
