"""The FastButton extends the Panel Button to a Fast Design Framework Button.

It is built on the the fast-button web component. The component supports several visual apperances
(accent, lightweight, neutral, outline, stealth).

For more information view the [component specification]\
(https://github.com/microsoft/fast/tree/master/packages/web-components/fast-foundation/\
src/button/button.spec.md).

See also https://explore.fast.design/components/fast-button.
    """
import param
from panel.widgets import Button
from awesome_panel_extensions.bokeh_extensions.fast_button import FastButton as _BkFastButton

FAST_BUTTON_APPEARENCES = [
    "accent",
    "lightweight",
    "neutral",
    "outline",
    "stealth",
]
DEFAULT_FAST_BUTTON_APPEARANCE = "neutral"
BUTTON_TYPE_TO_APPEARANCE = {
    "default": "neutral",
    "primary": "accent",
    "success": "outline",
    "warning": "accent",
    "danger": "accent",
}


class FastButton(Button):
    """The FastButton extends the Panel Button into the Fast Design Framework.

It is built on the the fast-button web component. The component supports several visual apperances
(accent, lightweight, neutral, outline, stealth).

For more information view the [component specification]\
(https://github.com/microsoft/fast/tree/master/packages/web-components/fast-foundation/\
src/button/button.spec.md).

See also https://explore.fast.design/components/fast-button.
    """
    appearance = param.ObjectSelector(
        default=DEFAULT_FAST_BUTTON_APPEARANCE,
        objects=FAST_BUTTON_APPEARENCES,
        doc="The appearance attribute",
        allow_None=True,
    )
    autofocus = param.Boolean(default=False, doc="The autofocus attribute",)

    _widget_type = _BkFastButton

    def __init__(self, **params):
        if "button_type" in params and "appearance" not in params:
            params["appearance"] = BUTTON_TYPE_TO_APPEARANCE[params["button_type"]]
        super().__init__(**params)

    @param.depends("button_type", watch=True)
    def _update_accent(self, *_):
        self.appearance = BUTTON_TYPE_TO_APPEARANCE[self.button_type]
