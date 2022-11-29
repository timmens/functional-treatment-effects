import pandas as pd
import pytask
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import SHOE_TYPE
from functional_treatment_effects.config import SRC
from functional_treatment_effects.data_management import create_indicator
from functional_treatment_effects.data_management import INDEX_COLS
from functional_treatment_effects.data_management import tidy_up_ankle_moments


@pytask.mark.depends_on(SRC.joinpath("data", "ankle_moments.csv"))
@pytask.mark.produces(BLD.joinpath("data", "all", "tidy_ankle_moments.csv"))
def task_create_tidy_ankle_moments(depends_on, produces):
    df = pd.read_csv(depends_on, index_col=INDEX_COLS["ankle_moments"])
    df_tidy = tidy_up_ankle_moments(df)
    df_tidy.to_csv(produces)


@pytask.mark.depends_on(SRC.joinpath("data", "strike_index.csv"))
@pytask.mark.produces(BLD.joinpath("data", "all", "strike_indicator.csv"))
def task_create_strike_indicator(depends_on, produces):
    df = pd.read_csv(depends_on, index_col=INDEX_COLS["strike_index"])
    df["strike_indicator"] = create_indicator(df.strike_index, cutoff=1 / 3)
    df.drop(columns=["strike_index"]).to_csv(produces)


for data_set in ("ankle_moments", "strike_indicator", "tidy_ankle_moments"):

    if data_set == "ankle_moments":
        depends_on = SRC.joinpath("data", f"{data_set}.csv")
    else:
        depends_on = BLD.joinpath("data", "all", f"{data_set}.csv")

    kwargs = {
        "depends_on": depends_on,
        "produces": BLD.joinpath("data", f"{data_set}.csv"),
        "data_set": data_set,
    }

    @pytask.mark.task(id=f"{data_set}", kwargs=kwargs)
    def task_filter_data(depends_on, produces, data_set):
        df = pd.read_csv(depends_on, index_col=INDEX_COLS[data_set])
        filtered = df.loc[SHOE_TYPE]
        filtered.to_csv(produces)
