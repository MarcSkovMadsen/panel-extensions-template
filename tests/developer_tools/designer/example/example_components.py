import altair as alt
import hvplot.pandas
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from panel.pane import plotly


def get_plotly_carshare_data():
    return px.data.carshare()


def plotly_carshare_plot(carshare):
    fig = px.scatter_mapbox(
        carshare,
        lat="centroid_lat",
        lon="centroid_lon",
        color="peak_hour",
        size="car_hours",
        color_continuous_scale=px.colors.cyclical.Phase,
        size_max=15,
        zoom=10,
        mapbox_style="carto-positron",
    )
    # Panel does currently not plot responsive Plotly plots well
    # https://github.com/holoviz/panel/issues/1514
    fig.layout.autosize = True
    return fig


def get_altair_bar_data():
    return pd.DataFrame(
        {
            "project": ["a", "b", "c", "d", "e", "f", "g"],
            "score": [25, 57, 23, 19, 8, 47, 8],
            "goal": [25, 47, 30, 27, 38, 19, 4],
        }
    )


def altair_bar_plot(data):
    bar_chart = alt.Chart(data).mark_bar().encode(x="project", y="score")

    tick_chart = (
        alt.Chart(data)
        .mark_tick(color="red", thickness=2, size=40 * 0.9,)  # controls width of tick.
        .encode(x="project", y="goal")
    )

    return (bar_chart + tick_chart).properties(width="container", height="container")


def matplotlib_plot():
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    FigureCanvas(fig)  # not needed for mpl >= 3.1

    X, Y, Z = axes3d.get_test_data(0.05)
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contourf(X, Y, Z, zdir="z", offset=-100, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir="x", offset=-40, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir="y", offset=40, cmap=cm.coolwarm)

    ax.set_xlabel("X")
    ax.set_xlim(-40, 40)
    ax.set_ylabel("Y")
    ax.set_ylim(-40, 40)
    ax.set_zlabel("Z")
    ax.set_zlim(-100, 100)
    return fig


def get_holoviews_plot(data):
    data = data.set_index("Year").drop("Annual", axis=1).transpose()
    return data.hvplot.heatmap(
        x="columns",
        y="index",
        title="US Unemployment 1948—2016",
        cmap=[
            "#75968f",
            "#a5bab7",
            "#c9d9d3",
            "#e2e2e2",
            "#dfccce",
            "#ddb7b1",
            "#cc7878",
            "#933b41",
            "#550b1d",
        ],
        xaxis="top",
        rot=70,
        responsive=True,
        height=800,
    ).opts(toolbar=None, fontsize={"title": 10, "xticks": 5, "yticks": 5},)
