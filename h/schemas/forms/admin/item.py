import colander
from deform.widget import MoneyInputWidget, SelectWidget, TextInputWidget

import h.i18n
from h.schemas.base import CSRFSchema

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def item_level_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select level --'),] + kwargs['level'])


@colander.deferred
def item_term_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select term --'),] + kwargs['term'])


class CostItemCreateSchema(CSRFSchema):
    number = colander.SchemaNode(
        colander.String(),
        title=_("No."),
        widget=TextInputWidget(),
    )

    name = colander.SchemaNode(colander.String(), title=_("Name"))

    price = colander.SchemaNode(
        colander.Money(),
        title=_("Current Price"),
        widget=MoneyInputWidget(),
    )

    comments = colander.SchemaNode(
        colander.String(),
        title=_("Comments"),
        widget=TextInputWidget(),
        missing=""
    )

    level = colander.SchemaNode(
        colander.String(),
        title=_("Class Level"),
        widget=item_level_select_widget,
        missing=None,
    )

    term = colander.SchemaNode(
        colander.String(),
        title=_("Term"),
        widget=item_term_select_widget,
        missing=None,
    )


class CostItemEditSchema(CSRFSchema):
    number = colander.SchemaNode(
        colander.String(),
        title=_("No."),
        widget=TextInputWidget(),
    )

    name = colander.SchemaNode(colander.String(), title=_("Name"))

    price = colander.SchemaNode(
        colander.Money(),
        title=_("Current Price"),
        widget=MoneyInputWidget(),
    )

    gst_included = colander.SchemaNode(
        colander.Money(),
        title=_("GST included"),
        widget=MoneyInputWidget(),
    )

    comments = colander.SchemaNode(
        colander.String(),
        title=_("Comments"),
        widget=TextInputWidget(),
        missing=""
    )

    level = colander.SchemaNode(
        colander.String(),
        title=_("Class Level"),
        widget=item_level_select_widget,
        missing=None,
    )

    term = colander.SchemaNode(
        colander.String(),
        title=_("Term"),
        widget=item_term_select_widget,
        missing=None,
    )
