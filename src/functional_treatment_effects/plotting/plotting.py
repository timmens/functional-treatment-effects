import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go


def plot_ic_illustration():

    funcs = {
        "linear": lambda x: 1 - x,
        "quadratic": lambda x: 1 - x**2,
        "matern": lambda x: np.exp(-x),
        "rational_quadratic": lambda x: (1 + x**2) ** (-1),
        "exponential": lambda x: np.exp(-(x**2)),
    }
    formulae = {
        "linear": r"$1 - x$",
        "quadratic": r"$1 - x^2$",
        "matern": r"$\exp(-|x|)$",
        "rational_quadratic": r"$(1 + x^2)^{-1}$",
        "exponential": r"$\exp(-|x|^2)$",
    }

    x = np.linspace(0, 0.5, num=100)
    data = pd.DataFrame({"x": x})

    for name, f in funcs.items():
        data[name] = f(x)

    data = data.melt(id_vars="x", var_name="type")

    fig = px.line(data, x="x", y="value", color="type", width=400)

    fig = fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        xaxis={
            "showticklabels": False,
        },
        yaxis={
            "showticklabels": False,
        },
        template="simple_white",
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
    )

    fig.add_annotation(
        x=0.2,
        y=funcs["linear"](0.2) - 0.015,
        text=formulae["linear"],
        textangle=50,
        showarrow=False,
    )
    fig.add_annotation(
        x=0.35,
        y=funcs["quadratic"](0.35) - 0.015,
        text=formulae["quadratic"],
        textangle=40,
        showarrow=False,
    )
    fig.add_annotation(
        x=0.25,
        y=funcs["matern"](0.25) + 0.025,
        text=formulae["matern"],
        textangle=40,
        showarrow=False,
    )
    fig.add_annotation(
        x=0.35,
        y=funcs["rational_quadratic"](0.35) + 0.025,
        text=formulae["rational_quadratic"],
        textangle=30,
        showarrow=False,
    )
    fig.add_annotation(
        x=0.45,
        y=funcs["exponential"](0.45),
        text=formulae["exponential"],
        textangle=20,
        showarrow=True,
        ax=-20,
        ay=70,
        arrowhead=1,
    )

    fig.update_annotations(font_size=100)
    fig.update_traces(line_width=3)
    fig.update_xaxes(linewidth=2)
    fig.update_yaxes(linewidth=2)

    fig.add_trace(go.Scatter(x=x, y=funcs["quadratic"](x), line_width=0))
    fig.add_trace(
        go.Scatter(
            x=x,
            y=funcs["matern"](x),
            line_width=0,
            fill="tonexty",
            fillpattern_shape="/",
            fillpattern_fillmode="replace",
        )
    )

    return fig


def plot_scb_illustration():
    x = np.linspace(0, 1, num=100)

    effect = np.sin(2 * np.pi * x) + 3 * x

    lower = effect - 0.75 * (1 + x)
    upper = effect + 0.75 * (1 + x)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=upper,
            line={"width": 0.5, "color": "steelblue"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=lower,
            fill="tonexty",
            line={"width": 0.5, "color": "steelblue"},
        )
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        font={"size": 25},
        xaxis={
            "showticklabels": False,
        },
        yaxis={
            "showticklabels": False,
        },
        template="simple_white",
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
    )
    fig.add_trace(go.Scatter(x=x, y=effect, line_color="goldenrod", line_width=4))
    return fig


def plot_doubly_robust_band(df, other):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=other, line={"width": 2, "color": "gray"}))
    fig.add_trace(
        go.Scatter(
            x=df.index.to_list() + df.index.to_list()[::-1],
            y=df.upper.to_list() + df.lower.to_list()[::-1],
            fill="toself",
            line={"width": 0.5, "color": "steelblue"},
        )
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df.estimate, line_color="goldenrod", line_width=5)
    )

    fig.add_annotation(x=8, y=0.3, text=r"$Nm/Kg$", showarrow=False, font_size=22)

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        font={"size": 25},
        xaxis={
            "tickmode": "array",
            "tickvals": [0, 100, 200],
            "ticktext": [0, 0.5, 1],
            "tickfont": {"size": 25},
        },
        template=None,
        showlegend=False,
    )

    return fig


def plot_data_presentation(data, indicator):

    data = data.query("variable == 'x'")
    data = data.reset_index()

    indicator["strike_indicator"] = indicator["strike_indicator"].map(
        {0: "Heel", 1: "Forefoot"}
    )

    data = data.merge(indicator)

    forefoot = (
        data.query("strike_indicator == 'Forefoot'").groupby("time")["moment"].mean()
    )
    heel = data.query("strike_indicator == 'Heel'").groupby("time")["moment"].mean()
    time = heel.to_frame().index

    fig = px.line(
        data,
        x="time",
        y="moment",
        line_group="id",
        color="strike_indicator",
        template="simple_white",
        color_discrete_map={
            "Heel": "goldenrod",
            "Forefoot": "steelblue",
        },
    )

    fig = fig.add_trace(
        go.Scattergl(
            x=time, y=forefoot, line_color="black", line_width=3, showlegend=False
        )
    )
    fig = fig.add_trace(
        go.Scattergl(x=time, y=heel, line_color="black", line_width=3, showlegend=False)
    )

    fig = fig.update_traces(opacity=0.5)

    fig.add_annotation(x=8, y=0.4, text=r"$Nm/Kg$", showarrow=False, font_size=22)

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        font={"size": 22},
        xaxis={
            "tickmode": "array",
            "tickvals": [0, 100, 200],
            "ticktext": [0, 0.5, 1],
            "tickfont": {"size": 25},
        },
        legend={
            "yanchor": "top",
            "y": 0.9,
            "xanchor": "left",
            "x": 0.45,
            "title": "",
            "font_size": 25,
        },
    )
    return fig


def plot_functional_sample(
    df, color_discrete_sequence=None, *, y="moment", opacity=0.2
):
    df = df.reset_index()
    if not {"time", "id"} <= set(df.columns):
        msg = "'time' and 'id' needs to be either a column or an index of df."
        raise ValueError(msg)
    fig = px.line(
        df,
        x="time",
        y=y,
        color="id",
        template="simple_white",
        color_discrete_sequence=color_discrete_sequence,
    )
    update_traces_kwargs = {"opacity": opacity}
    if color_discrete_sequence is None:
        update_traces_kwargs["line_color"] = "black"
    fig = fig.update_traces(**update_traces_kwargs)
    fig = fig.update_layout(showlegend=False)
    return fig


def plot_df_with_time_axis(df):
    if "time" not in df:
        if "time" in df.index.names:
            df = df.reset_index()
        else:
            msg = "df does not contain a time index."
            raise ValueError(msg)

    fig = px.line(df, x="time", y=df.columns, template="simple_white")
    return fig


def plot_dag(path):
    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            (r"$X_{i1}$", r"$W_i$"),
            (r"$X_{i2}$", r"$W_i$"),
            (r"$X_{i2}$", r"$Y_i(t)$"),
            (r"$X_{i3}$", r"$Y_i(t)$"),
            (r"$X_{i4}(t)$", r"$Y_i(t)$"),
            (r"$W_i$", r"$Y_i(t)$"),
        ]
    )

    options = {
        "font_size": 22,
        "node_size": 4000,
        "node_color": ["white", "lightblue", "white", "gold", "white", "white"],
        "edgecolors": "#455A64",
        "font_color": "#455A64",
        "edge_color": "#455A64",
        "linewidths": 2,
        "width": 2,
    }

    nx.draw_shell(graph, with_labels=True, **options)

    ax = plt.gca()
    plt.axis("off")
    ax.margins(0.10)
    plt.savefig(path)
