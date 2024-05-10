import colander
import datetime
from deform.widget import SelectWidget, TextInputWidget

import h.i18n
from h.schemas.base import CSRFSchema
from h.schemas.forms.widgets import DateInputWidget

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def registeration_gender_select_widget(_node, kwargs):
    return SelectWidget(values=(('', 'Select gender'), ('Male', 'Male'), ('Female', 'Female')),)


@colander.deferred
def registeration_code_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs['code'])


@colander.deferred
def registeration_level_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs['level'])


@colander.deferred
def registeration_term_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs['term'])


@colander.deferred
def registeration_source_select_widget(_node, kwargs):
    return SelectWidget(values=kwargs['source'])


class RegistrationOptionSchema(CSRFSchema):
    name = colander.SchemaNode(colander.String(), title=_("Name"))

    chinese = colander.SchemaNode(colander.String(), title=_("Chinese"))


class RegistrationSchema(CSRFSchema):
    last_name = colander.SchemaNode(colander.String(), title=_("Given name"))
    first_name = colander.SchemaNode(colander.String(), title=_("Family name"))
    date_of_birth = colander.SchemaNode(
        colander.Date(),
        title=_("Date of Birth"),
        default=datetime.datetime.today(),
        widget=DateInputWidget(),
    )

    gender = colander.SchemaNode(
        colander.String(),
        title=_("Gender"),
        widget=registeration_gender_select_widget,
    )

    code = colander.SchemaNode(
        colander.String(),
        title=_("Class Location & Time"),
        widget=registeration_code_select_widget,
    )

    level = colander.SchemaNode(
        colander.String(),
        title=_("Class Level"),
        widget=registeration_level_select_widget,
    )

    term = colander.SchemaNode(
        colander.String(),
        title=_("Length Options (discounts applies to payments for more than 2 full terms)"),
        widget=registeration_term_select_widget,
    )

    email = colander.SchemaNode(
        colander.String(),
        title=_("Email"),
        widget=TextInputWidget(),
        missing=""
    )

    first_emergency_contact = colander.SchemaNode(
        colander.String(),
        title=_("Parent 1 Phone No."),
        widget=TextInputWidget(),
    )

    second_emergency_contact = colander.SchemaNode(
        colander.String(),
        title=_("Parent 2 Phone No."),
        widget=TextInputWidget(),
        missing=""
    )

    emergency_contact = colander.SchemaNode(
        colander.String(),
        title=_("Emergency Contact"),
        widget=TextInputWidget(),
        missing=""
    )

    wechat = colander.SchemaNode(
        colander.String(),
        title=_("Wechat"),
        widget=TextInputWidget(),
        missing=""
    )

    source = colander.SchemaNode(
        colander.String(),
        title=_("How did you find us?"),
        widget=registeration_source_select_widget,
    )

    referer = colander.SchemaNode(
        colander.String(),
        title=_("Referral person (Existing student number or parent contact)"),
        widget=TextInputWidget(),
        missing=""
    )

    memeo = colander.SchemaNode(
        colander.String(),
        title=_("Your Message"),
        widget=TextInputWidget(),
        missing=""
    )
