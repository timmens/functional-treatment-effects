import pandas as pd
import pytask
from functional_treatment_effects.confidence_bands.bands import estimate_confidence_band
from functional_treatment_effects.config import BLD
from functional_treatment_effects.data_management import INDEX_COLS
from functional_treatment_effects.fitting.fitting import get_fitter


fit_func_on_scalar = get_fitter(fitter="func_on_scalar")
fit_doubly_robust = get_fitter(fitter="func_on_scalar_doubly_robust")


@pytask.mark.depends_on(
    {
        "x": BLD.joinpath("data/bare/strike_indicator.csv"),
        "y": BLD.joinpath("data/bare/ankle_moments.csv"),
    }
)
@pytask.mark.produces(BLD.joinpath("models/bare/coef.csv"))
def task_fit_model(depends_on, produces):
    x_index_cols = list(set(INDEX_COLS["strike_indicator"]) - {"shoe_type"})
    y_index_cols = list(set(INDEX_COLS["ankle_moments"]) - {"shoe_type"})
    x = pd.read_csv(depends_on["x"], index_col=x_index_cols)
    y = pd.read_csv(depends_on["y"], index_col=y_index_cols)
    y = y.query("variable == 'x'")

    coef = fit_func_on_scalar(x=x, y=y, fit_intercept=True)

    coef.to_csv(produces)


@pytask.mark.depends_on(
    {
        "x": BLD.joinpath("data/bare/subject_information.csv"),
        "t": BLD.joinpath("data/bare/strike_indicator.csv"),
        "y": BLD.joinpath("data/bare/ankle_moments.csv"),
    }
)
@pytask.mark.produces(BLD.joinpath("models/bare/doubly_robust.csv"))
def task_fit_doubly_robust(depends_on, produces):
    t_index_cols = list(set(INDEX_COLS["strike_indicator"]) - {"shoe_type"})
    y_index_cols = list(set(INDEX_COLS["ankle_moments"]) - {"shoe_type"})
    t = pd.read_csv(depends_on["t"], index_col=t_index_cols)
    y = pd.read_csv(depends_on["y"], index_col=y_index_cols)
    x = pd.read_csv(depends_on["x"], index_col=INDEX_COLS["subject_information"])
    y = y.query("variable == 'x'")

    controls = [
        "gender",
        "foot_shape",
        "age",
        "weekly_km",
        "toe_flex_strength",
        "plantar_flex_strength",
        "knee_exten_strength",
    ]
    x = x[controls]
    x = pd.get_dummies(x).dropna()

    y = y.droplevel(level="variable", axis=0).loc[x.index]
    t = t.loc[x.index]

    res = fit_doubly_robust(x=x, y=y, t=t)

    band = estimate_confidence_band(
        res["effect"].values.flatten(), res["kernel"] / 10, n_samples=112, n_points=201
    )

    effect = res["effect"]
    effect["lower"] = band.lower
    effect["upper"] = band.upper
    effect["estimate"] = band.estimate

    effect = effect.drop(columns=["value"])
    effect.to_csv(produces)
