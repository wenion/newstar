import codecs
import colander
import deform
from functools import lru_cache
import logging

from h import i18n, models
from h.models.user import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    USERNAME_PATTERN,
)
from h.schemas import validators
from h.schemas.base import CSRFSchema

_ = i18n.TranslationString
log = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_blacklist():
    # Try to load the blacklist file from disk. If, for whatever reason, we
    # can't load the file, then don't crash out, just log a warning about
    # the problem.
    try:
        with codecs.open("h/accounts/blacklist", encoding="utf-8") as handle:
            blacklist = handle.readlines()
    except (IOError, ValueError):  # pragma: no cover
        log.exception("unable to load blacklist")
        blacklist = []
    return set(line.strip().lower() for line in blacklist)


def unique_username(node, value):
    """Colander validator that ensures the username does not exist."""
    request = node.bindings["request"]
    user = models.User.get_by_username(request.db, value, request.default_authority)
    if user:  # pragma: no cover
        msg = _("This username is already taken.")
        raise colander.Invalid(node, msg)


def unique_email(node, value):
    """Colander validator that ensures no user with this email exists."""
    request = node.bindings["request"]
    user = models.User.get_by_email(request.db, value, request.default_authority)
    if user and user.userid != request.authenticated_userid:
        msg = _("Sorry, an account with this email address already exists.")
        raise colander.Invalid(node, msg)


def email_node(**kwargs):
    """Return a Colander schema node for a new user email."""
    return colander.SchemaNode(
        colander.String(),
        validator=colander.All(
            validators.Length(max=EMAIL_MAX_LENGTH), validators.Email(), unique_email
        ),
        widget=deform.widget.TextInputWidget(
            template="emailinput", autocomplete="username"
        ),
        **kwargs
    )


def unblacklisted_username(node, value, blacklist=None):
    """Colander validator that ensures the username is not blacklisted."""
    if blacklist is None:
        blacklist = get_blacklist()
    if value.lower() in blacklist:
        # We raise a generic "user with this name already exists" error so as
        # not to make explicit the presence of a blacklist.
        msg = _(
            "Sorry, an account with this username already exists. "
            "Please enter another one."
        )
        raise colander.Invalid(node, msg)


class RegisterSchema(CSRFSchema):
    username = colander.SchemaNode(
        colander.String(),
        validator=colander.All(
            validators.Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH),
            colander.Regex(
                USERNAME_PATTERN,
                msg=_("Must have only letters, numbers, periods, and underscores."),
            ),
            unique_username,
            unblacklisted_username,
        ),
        title=_("Username"),
        hint=_(
            "Must be between {min} and {max} characters, containing only "
            "letters, numbers, periods, and underscores."
        ).format(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH),
        widget=deform.widget.TextInputWidget(autofocus=True),
    )
    email = email_node(title=_("Email address"))