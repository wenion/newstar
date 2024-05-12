import colander
import datetime
from deform.widget import SelectWidget, TextInputWidget

import h.i18n
from h.schemas.base import CSRFSchema
from h.schemas.forms.widgets import DateInputWidget

_ = h.i18n.TranslationString

# TODO validator
@colander.deferred
def registration_gender_select_widget(_node, kwargs):
    return SelectWidget(values=(('', '-- Select gender --'), ('Male', 'Male'), ('Female', 'Female')),)


@colander.deferred
def profile_registration_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select registration --'),] + kwargs['registration'])


@colander.deferred
def profile_registration_restricted_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select registration --'),] + kwargs['registration'], readonly=True)


@colander.deferred
def profile_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select account --'),] + kwargs['profile'])


@colander.deferred
def profile_user_select_widget(_node, kwargs):
    return SelectWidget(values=[('', '-- Select account --'),] + kwargs['user'])


class ProfileSchema(CSRFSchema):
    number = colander.SchemaNode(
        colander.String(),
        title=_("No."),
        widget=TextInputWidget(),
    )

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
        widget=registration_gender_select_widget,
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

    phone = colander.SchemaNode(
        colander.String(),
        title=_("Phone"),
        widget=TextInputWidget(),
        missing=""
    )

    registration = colander.SchemaNode(
        colander.String(),
        title=_("Enroll Information"),
        widget=profile_registration_select_widget,
    )

    referer = colander.SchemaNode(
        colander.String(),
        title=_("Referral person"),
        widget=profile_select_widget,
        missing=None
    )

    user = colander.SchemaNode(
        colander.String(),
        title=_("Account"),
        widget=profile_user_select_widget,
        missing=None
    )

    memeo = colander.SchemaNode(
        colander.String(),
        title=_("Your Message"),
        widget=TextInputWidget(),
        missing=""
    )
