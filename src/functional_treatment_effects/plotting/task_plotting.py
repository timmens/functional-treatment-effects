import pandas as pd
import pytask
from functional_treatment_effects.config import BLD
from functional_treatment_effects.data_management import INDEX_COLS
from functional_treatment_effects.plotting.plotting import plot_dag
from functional_treatment_effects.plotting.plotting import plot_data_presentation
from functional_treatment_effects.plotting.plotting import plot_df_with_time_axis
from functional_treatment_effects.plotting.plotting import plot_doubly_robust_band
from functional_treatment_effects.plotting.plotting import plot_functional_sample


@pytask.mark.depends_on(
    {
        "data": BLD.joinpath("data", "tidy_ankle_moments.csv"),
        "colors": BLD.joinpath("data", "strike_indicator.csv"),
    }
)
@pytask.mark.produces(BLD.joinpath("figures", "ankle_moments_y.png"))
def task_plot_sample(depends_on, produces):
    index_cols = list(set(INDEX_COLS["ankle_moments"]) - {"shoe_type"})
    df = pd.read_csv(depends_on["data"], index_col=index_cols)

    indicator = pd.read_csv(depends_on["colors"])
    colors = indicator.strike_indicator.map(
        lambda x: "goldenrod" if x == 0 else "steelblue"
    ).values

    fig = plot_functional_sample(df, color_discrete_sequence=colors, opacity=0.3)
    fig.write_image(produces)


for estimator in ("linear_model", "doubly_robust"):

    @pytask.mark.depends_on(BLD.joinpath("models", f"{estimator}_estimate.pickle"))
    @pytask.mark.produces(BLD.joinpath("figures", f"{estimator}_effect.png"))
    @pytask.mark.task(id=estimator)
    def task_plot_effect(depends_on, produces):
        res = pd.read_pickle(depends_on)
        if "slopes" in res:
            df = res["slopes"]
        elif "treatment_effect" in res:
            df = res["treatment_effect"]
        fig = plot_df_with_time_axis(df)
        fig.write_image(produces)


@pytask.mark.depends_on(
    {
        "data": BLD.joinpath("data", "tidy_ankle_moments.csv"),
        "strike_indicator": BLD.joinpath("data", "strike_indicator.csv"),
    }
)
@pytask.mark.produces(BLD.joinpath("figures", "presentation", "data.png"))
def task_plot_data_presentation(depends_on, produces):
    indicator = pd.read_csv(depends_on["strike_indicator"])

    index_cols = list(set(INDEX_COLS["ankle_moments"]) - {"shoe_type"})
    data = pd.read_csv(depends_on["data"], index_col=index_cols)

    fig = plot_data_presentation(data, indicator)
    fig.write_image(produces, width=1400, height=700)


@pytask.mark.depends_on(BLD.joinpath("models", "doubly_robust.csv"))
@pytask.mark.produces(BLD.joinpath("figures", "presentation", "doubly_robust.png"))
def task_plot_doubly_robust_band(depends_on, produces):
    df = pd.read_csv(depends_on, index_col="time")
    fig = plot_doubly_robust_band(df)
    fig.write_image(produces, width=1400, height=700)


@pytask.mark.produces(BLD.joinpath("figures", "presentation", "dag.png"))
def task_plot_dag(produces):
    plot_dag(produces)
