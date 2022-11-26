import pandas as pd
import pytask
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import SRC
from functional_treatment_effects.data_management import create_indicator
from functional_treatment_effects.data_management import INDEX_COLS
from functional_treatment_effects.data_management import SHOE_TYPES
from functional_treatment_effects.data_management import tidy_up_ankle_moments


@pytask.mark.depends_on(SRC.joinpath("data", "ankle_moments.csv"))
@pytask.mark.produces(BLD.joinpath("data", "tidy_ankle_moments.csv"))
def task_create_tidy_ankle_moments(depends_on, produces):
    df = pd.read_csv(depends_on, index_col=INDEX_COLS["ankle_moments"])
    df_tidy = tidy_up_ankle_moments(df)
    df_tidy.to_csv(produces)


@pytask.mark.depends_on(SRC.joinpath("data", "strike_index.csv"))
@pytask.mark.produces(BLD.joinpath("data", "strike_indicator.csv"))
def task_create_strike_indicator(depends_on, produces):
    df = pd.read_csv(depends_on, index_col=INDEX_COLS["strike_index"])
    df["strike_indicator"] = create_indicator(df.strike_index, cutoff=1 / 3)
    df.drop(columns=["strike_index"]).to_csv(produces)


for shoe_type in SHOE_TYPES:

    for data_set in ("tidy_ankle_moments", "strike_indicator"):

        kwargs = {
            "depends_on": BLD.joinpath("data", f"{data_set}.csv"),
            "produces": BLD.joinpath("data", shoe_type, f"{data_set}.csv"),
            "shoe_type": shoe_type,
            "data_set": data_set,
        }

        @pytask.mark.task(id=f"{shoe_type}_{data_set}", kwargs=kwargs)
        def task_filter_data(depends_on, produces, shoe_type, data_set):
            df = pd.read_csv(depends_on, index_col=INDEX_COLS[data_set])
            filtered = df.loc[shoe_type]
            filtered.to_csv(produces)
