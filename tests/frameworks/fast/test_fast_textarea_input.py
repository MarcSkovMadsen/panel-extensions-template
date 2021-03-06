# pylint: disable=redefined-outer-name,protected-access
# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring
from awesome_panel_extensions.frameworks.fast import FastTextAreaInput
from tests.frameworks.fast.fast_test_app import create_fast_test_app


def test_can_construct_with_defaults():
    # When
    textinput = FastTextAreaInput()
    # Then
    assert textinput.name == ""
    assert textinput.value == ""
    assert textinput.placeholder == ""
    assert textinput.max_length == 5000
    assert textinput.disabled is False

    assert textinput.appearance is None
    assert textinput.autofocus is False
    assert textinput.resize is None
    assert textinput.cols == 20
    assert textinput.rows == 2
    assert textinput.spellcheck is False
    assert textinput.min_length == 0
    assert textinput.required is False
    assert textinput.readonly is False


def test_view():
    textinput = FastTextAreaInput(name="Be Fast!", placeholder="Write something!")
    app = create_fast_test_app(
        component=textinput,
        parameters=[
            "name",
            "value",
            "placeholder",
            "max_length",
            "disabled",
            "appearance",
            "autofocus",
            "resize",
            "cols",
            "rows",
            "spellcheck",
            "min_length",
            "required",
            "readonly",
        ],
    )
    return app


if __name__.startswith("bokeh"):
    test_view().servable()
