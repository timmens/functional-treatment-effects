import pandas as pd
import pytask
from fte.confidence_bands.bands import estimate_confidence_band
from fte.fitting.fitting import get_fitter
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import SRC
from functional_treatment_effects.data_management import INDEX_COLS


@pytask.mark.depends_on(
    {
        "treatment_status": BLD.joinpath("data", "strike_indicator.csv"),
        "y": BLD.joinpath("data", "ankle_moments.csv"),
    }
)
@pytask.mark.produces(BLD.joinpath("models", "linear_model_estimate.pickle"))
def task_fit_linear_model(depends_on, produces):
    # read data
    # ==================================================================================
    treatment_status = pd.read_csv(depends_on["treatment_status"], index_col=["id"])
    y = pd.read_csv(depends_on["y"], index_col=["variable", "id"])
    y = y.loc["x"]

    # fit model
    # ==================================================================================
    fit_method = get_fitter(fitter="func_on_scalar")

    res = fit_method(x=treatment_status, y=y, fit_intercept=True)

    # write results
    # ==================================================================================
    pd.to_pickle(res, produces)


@pytask.mark.depends_on(
    {
        "treatment_status": BLD.joinpath("data", "strike_indicator.csv"),
        "x": SRC.joinpath("data", "subject_information.csv"),
        "y": BLD.joinpath("data", "ankle_moments.csv"),
    }
)
@pytask.mark.produces(BLD.joinpath("models", "doubly_robust_estimate.pickle"))
def task_fit_doubly_robust(depends_on, produces):
    # read data
    # ==================================================================================
    treatment_status = pd.read_csv(depends_on["treatment_status"], index_col=["id"])

    x = pd.read_csv(depends_on["x"], index_col=INDEX_COLS["subject_information"])
    x = x.drop(columns=["name"])

    y = pd.read_csv(depends_on["y"], index_col=["variable", "id"])
    y = y.loc["x"]

    # data preparation
    # ==================================================================================
    x = pd.get_dummies(x).dropna()
    y = y.loc[x.index]
    treatment_status = treatment_status.loc[x.index]

    # fit model
    # ==================================================================================
    fit_method = get_fitter(fitter="func_on_scalar_doubly_robust")

    res = fit_method(x=x, y=y, t=treatment_status)

    # write results
    # ==================================================================================
    pd.to_pickle(res, produces)


for estimator in ("linear_model", "doubly_robust"):

    @pytask.mark.skipif(estimator == "linear_model", reason="Not implemented yet.")
    @pytask.mark.depends_on(BLD.joinpath("models", f"{estimator}_estimate.pickle"))
    @pytask.mark.produces(BLD.joinpath("models", f"{estimator}.csv"))
    @pytask.mark.task(id=estimator)
    def task_compute_confidence_band(depends_on, produces):
        # read data
        # ==================================================================================
        res = pd.read_pickle(depends_on)

        # compute confidence band
        # ==================================================================================
        effect = res["treatment_effect"]
        band = estimate_confidence_band(
            estimate=effect.values.flatten(),
            cov=res["cov"] / res["n_samples"],
            n_samples=res["n_samples"],
            numerical_options={"raise_error": False},
        )

        res = pd.DataFrame(band._asdict()).set_index(effect.index)

        # write results
        # ==================================================================================
        res.to_csv(produces)
