import json

from colander import Mapping, SchemaNode
from colander import String
from deform.compat import string_types, text_
from deform.widget import Widget


_BLANK = text_("")


class _null:
    """Represents a null value in colander-related operations."""

    def __nonzero__(self):
        return False

    # py3 compat
    __bool__ = __nonzero__

    def __repr__(self):
        return '<colander.null>'

    def __reduce__(self):
        return 'null'  # when unpickled, refers to "null" below (singleton)


null = _null()



class _PossiblyEmptyString(String):
    def deserialize(self, node, cstruct):
        if cstruct == "":
            return _BLANK  # String.deserialize returns null
        return super(_PossiblyEmptyString, self).deserialize(node, cstruct)


class _StrippedString(_PossiblyEmptyString):
    def deserialize(self, node, cstruct):
        appstruct = super(_StrippedString, self).deserialize(node, cstruct)
        if isinstance(appstruct, string_types):
            appstruct = appstruct.strip()
        return appstruct


class DateInputWidget(Widget):
    """
    Renders a date picker widget.

    The default rendering is as a native HTML5 date input widget,
    falling back to pickadate (https://github.com/amsul/pickadate.js.)

    Most useful when the schema node is a ``colander.Date`` object.

    **Attributes/Arguments**

    options
        Dictionary of options for configuring the widget (eg: date format)

    template
        The template name used to render the widget.  Default:
        ``dateinput``.

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/textinput``.
    """

    template = "dateinput"
    readonly_template = "readonly/textinput"
    type_name = "date"
    requirements = (("modernizr", None), ("pickadate", None))
    default_options = (
        ("format", "yyyy-mm-dd"),
        ("selectMonths", True),
        ("selectYears", True),
    )
    options = None

    _pstruct_schema = Mapping()
    # SchemaNode(
    #     Mapping(),
    #     SchemaNode(_StrippedString(), name="date"),
    #     SchemaNode(_StrippedString(), name="date_submit", missing=""),
    # )

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ""
        readonly = kw.get("readonly", self.readonly)
        template = readonly and self.readonly_template or self.template
        options = dict(
            kw.get("options") or self.options or self.default_options
        )
        options["formatSubmit"] = "yyyy-mm-dd"
        kw.setdefault("options_json", json.dumps(options))
        values = self.get_template_values(field, cstruct, kw)
        return field.renderer(template, **values)

    def deserialize(self, field, pstruct):
        if pstruct in ("", null):
            return null
        return pstruct
        # try:
        #     validated = self._pstruct_schema.deserialize(pstruct)
        # except Invalid as exc:
        #     raise Invalid(field.schema, "Invalid pstruct: %s" % exc)
        # return validated["date_submit"] or validated["date"]
