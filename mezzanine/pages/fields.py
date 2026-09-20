from mezzanine.conf import settings
from mezzanine.core.fields import MultiChoiceField


class MenusField(MultiChoiceField):
    """
    ``MultiChoiceField`` for specifying which menus a page should appear in.
    """

    def __init__(self, *args, **kwargs):
        defaults = {"max_length": 100}
        defaults.update(kwargs)
        super().__init__(*args, **defaults)
        self._overridden_default = "default" in kwargs
        self._overridden_choices = "choices" in kwargs

    def has_default(self):
        """
        We either have a user-provided default or can determine one based on
        settings.
        """
        return True

    def get_default(self):
        """
        If the user provided a default in the field definition, returns it,
        otherwise determines the default menus based on available choices and
        ``PAGE_MENU_TEMPLATES_DEFAULT``. Ensures the default is not mutable.
        """
        if self._overridden_default:
            # Even with user-provided default we'd rather not have it
            # forced to text. Compare with Field.get_default().
            if callable(self.default):
                default = self.default()
            else:
                default = self.default
        else:
            # Depending on PAGE_MENU_TEMPLATES_DEFAULT:
            # * None or no value: all choosable menus;
            # * some sequence: specified menus;
            # (* empty sequence: no menus).
            default = getattr(settings, "PAGE_MENU_TEMPLATES_DEFAULT", None)
            if default is None:
                choices = self.get_choices(include_blank=False)
                default = (c[0] for c in choices)
        # Default can't be mutable, as references to it are shared among
        # model instances; all sane values should be castable to a tuple.
        return tuple(default)

    def _get_choices(self):
        """
        Returns menus specified in ``PAGE_MENU_TEMPLATES`` unless you provide
        some custom choices in the field definition.
        """
        if self._overridden_choices:
            # Note: choices is a property on Field bound to _get_choices().
            return self._choices
        else:
            menus = getattr(settings, "PAGE_MENU_TEMPLATES", [])
            return (m[:2] for m in menus)

    def deconstruct(self):
        """
        Materialise ``choices`` for deconstruction.

        ``MenusField.choices`` is a property returning a generator. Django
        <=4.2 unrolled an iterable ``choices`` value into a concrete list in
        ``Field.deconstruct()``; Django 5.0 removed that unrolling, so the
        generator is returned verbatim. The migration autodetector then sees a
        generator where the recorded migration state holds a tuple and emits
        the same ``AlterField`` on every run (0007, 0008, ... forever).

        Restoring the <=4.2 materialisation keeps the deconstructed field
        state stable and byte-identical to the recorded history, so no new
        migration identity is needed for the Django 5.2 endpoint. Behaviour is
        otherwise unchanged: the field still reads ``PAGE_MENU_TEMPLATES``
        lazily through ``choices``/``get_default``.
        """
        name, path, args, kwargs = super().deconstruct()
        if "choices" in kwargs:
            kwargs["choices"] = list(kwargs["choices"])
        return name, path, args, kwargs

    def _set_choices(self, choices):
        self._choices = choices

    choices = property(_get_choices, _set_choices)
