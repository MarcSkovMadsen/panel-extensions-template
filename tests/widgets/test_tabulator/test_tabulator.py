# pylint: disable=redefined-outer-name,protected-access
# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring
"""This module contains tests of the tabulator Data Grid"""

# http://tabulator.info/docs/4.7/quickstart
# https://github.com/paulhodel/jexcel

from logging import root
from awesome_panel_extensions.developer_tools.designer.services.component_reloader import (
    ComponentReloader,
)
import pandas as pd
import panel as pn
import param
import pytest
from bokeh.models import ColumnDataSource

from awesome_panel_extensions.developer_tools.designer import Designer
from awesome_panel_extensions.widgets.tabulator import (
    CSS_HREFS,
    JS_SRC,
    MOMENT_SRC,
    Tabulator,
    TabulatorStylesheet,
)


def _data_records():
    return [
        {"id": 1, "name": "Oli Bob", "age": 12, "col": "red", "dob": pd.Timestamp("14/05/1982")},
        {"id": 2, "name": "Mary May", "age": 1, "col": "blue", "dob": pd.Timestamp("14/05/1982")},
        {
            "id": 3,
            "name": "Christine Lobowski",
            "age": 42,
            "col": "green",
            "dob": pd.Timestamp("22/05/1982"),
        },
        {
            "id": 4,
            "name": "Brendon Philips",
            "age": 125,
            "col": "orange",
            "dob": pd.Timestamp("01/08/1980"),
        },
        {
            "id": 5,
            "name": "Margret Marmajuke",
            "age": 16,
            "col": "yellow",
            "dob": pd.Timestamp("31/01/1999"),
        },
    ]


@pytest.fixture()
def data_records():
    return _data_records()


@pytest.fixture()
def dataframe(data_records):
    return pd.DataFrame(data=data_records)


@pytest.fixture()
def data_list(dataframe):
    return dataframe.to_dict("list")


@pytest.fixture()
def column_data_source(data_list):
    return ColumnDataSource(data_list)


@pytest.fixture()
def columns():
    return [
        {
            "title": "Id",
            "field": "id",
            "sorter": "number",
            "formatter": "money",
            "hozAlign": "right",
        },
        {
            "title": "Name",
            "field": "name",
            "sorter": "plaintext",
            "formatter": "plaintext",
            "hozAlign": "left",
        },
        {
            "title": "Age",
            "field": "age",
            "sorter": "number",
            "formatter": "money",
            "hozAlign": "right",
        },
        {
            "title": "Col",
            "field": "col",
            "sorter": "plaintext",
            "formatter": "plaintext",
            "hozAlign": "left",
        },
        {
            "title": "Dob",
            "field": "dob",
            "sorter": "datetime",
            "formatter": "datetime",
            "hozAlign": "left",
        },
    ]


@pytest.fixture()
def configuration():
    # http://tabulator.info/docs/4.7/quickstart
    return {"autoColumns": True}


@pytest.fixture
def tabulator(configuration, dataframe):
    return Tabulator(configuration=configuration, value=dataframe)


def test_constructor():
    # When
    tabulator = Tabulator()
    # Then
    assert not tabulator.value
    assert isinstance(tabulator._source, ColumnDataSource)
    assert tabulator.configuration == {"autoColumns": True}
    assert tabulator.selection == []
    assert tabulator.selected_values is None


def test_tabulator_from_dataframe(dataframe, configuration):
    tabulator = Tabulator(value=dataframe, configuration=configuration)
    assert isinstance(tabulator._source, ColumnDataSource)


def test_tabulator_from_column_data_source(column_data_source, configuration):
    tabulator = Tabulator(value=column_data_source, configuration=configuration)
    assert tabulator._source == tabulator.value


def test_dataframe_to_columns_configuration(dataframe, columns):
    # Given
    value = dataframe
    # When
    actual = Tabulator.to_columns_configuration(value)
    # Then
    assert actual == columns


def test_config_default():
    # When
    Tabulator.config()
    # Then
    # assert pn.config.js_files["tabulator"] == JS_SRC
    # assert pn.config.js_files["moment"] == MOMENT_SRC
    assert CSS_HREFS["default"] in pn.config.css_files


def test_config_none():
    # Given
    css_count = len(pn.config.css_files)
    pn.config.js_files.clear()
    # When
    Tabulator.config(css=None, momentjs=False)
    # Then
    # assert pn.config.js_files["tabulator"] == JS_SRC
    # assert "moment" not in pn.config.js_files
    assert len(pn.config.css_files) == css_count


def test_config_custom():
    # When
    Tabulator.config(css="materialize")
    # Then
    # assert pn.config.js_files["tabulator"] == JS_SRC
    # assert pn.config.js_files["moment"] == MOMENT_SRC
    assert CSS_HREFS["materialize"] in pn.config.css_files


def test_selection_dataframe(data_records, dataframe):
    # Given
    tabulator = Tabulator(value=dataframe)
    # When
    tabulator.selection = [0, 1, 2]
    actual = tabulator.selected_values
    # Then
    expected = pd.DataFrame(data=data_records[0:3])
    pd.testing.assert_frame_equal(actual, expected)


def test_selection_column_data_source(data_records, column_data_source):
    # Given
    tabulator = Tabulator(value=column_data_source)
    # When
    tabulator.selection = [0, 1, 2]
    actual = tabulator.selected_values
    # Then
    # I could not find a more direct way to test this.
    expected_as_df = pd.DataFrame(data=data_records[0:3])
    pd.testing.assert_frame_equal(actual.to_df().drop(columns="index"), expected_as_df)


@pytest.mark.parametrize(
    ["field", "expected"],
    [("name", "Name"), ("cheese cake", "Cheese Cake"), ("cheese_cake", "Cheese Cake"),],
)
def test_to_title(field, expected):
    assert Tabulator._to_title(field) == expected


def test_tabulator_comms(document, comm, column_data_source, configuration):
    # Given
    tabulator = Tabulator(value=column_data_source, configuration=configuration)
    widget = tabulator.get_root(document, comm=comm)

    # Then
    assert isinstance(widget, tabulator._widget_type)
    assert widget.source == column_data_source
    assert widget.configuration == configuration

    # When
    tabulator._process_events(
        {"configuration": {"a": 1},}
    )

    # Then
    assert tabulator.configuration == {"a": 1}


def test_selected_change(tabulator):
    # When
    tabulator.selection = [2, 4, 6]
    # Then
    assert tabulator._source.selected.indices == [2, 4, 6]


def test_source_selection_change(tabulator):
    # When
    tabulator._process_events({"indices": [2, 4, 6]})
    # Then
    assert tabulator.selection == [2, 4, 6]


def test_tabulator_style_sheet():
    # When
    stylesheet = TabulatorStylesheet(theme="materialize")
    # Then
    assert stylesheet.object.startswith("<link rel=")
    assert CSS_HREFS["materialize"] in stylesheet.object
    assert stylesheet.object.endswith(">")

    # When
    stylesheet.theme = "site"
    assert CSS_HREFS["site"] in stylesheet.object


def test_cell_change_when_dataframe():
    # Given
    value = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    tabulator = Tabulator(value=value)
    original_data = tabulator._source.data
    # When
    tabulator._cell_change = {"c": "x", "i": 1, "v": 3}
    # Then
    assert tabulator.value.loc[1, "x"] == 3
    # And the tabulator._source.data shall not have been updated
    # We currently use the _updating_from_cell_value parameter to avoid reupdating the _source.data
    assert tabulator._source.data is original_data


def test_cell_change_when_column_data_sourc():
    # Given
    value = ColumnDataSource(pd.DataFrame({"x": [1, 2], "y": ["a", "b"]}))
    tabulator = Tabulator(value=value)
    # When
    tabulator._cell_change = {"c": "x", "i": 1, "v": 3}
    # Then we assume the columndatasource has been update on the js side
    # and therefore don't update on the python side
    assert tabulator.value.to_df().loc[1, "x"] == 2