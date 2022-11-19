import pandas as pd
import pytask
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import SRC
from functional_treatment_effects.data_management import create_strike_indicator
from functional_treatment_effects.data_management import create_tidy_ankle_moments
from functional_treatment_effects.data_management import DATA_SETS
from functional_treatment_effects.data_management import filter_by_shoe_type
from functional_treatment_effects.data_management import INDEX_COLS
from functional_treatment_effects.data_management import SHOE_TYPES


@pytask.mark.depends_on(SRC.joinpath("data/ankle_moments.csv"))
@pytask.mark.produces(BLD.joinpath("data/tidy_ankle_moments.csv"))
def task_create_tidy_ankle_moments(depends_on, produces):
    df = pd.read_csv(depends_on, index_col=INDEX_COLS["ankle_moments"])
    df_tidy = create_tidy_ankle_moments(df)
    df_tidy.to_csv(produces)


@pytask.mark.depends_on(SRC.joinpath("data/strike_index.csv"))
@pytask.mark.produces(BLD.joinpath("data/strike_indicator.csv"))
def task_create_strike_indicator(depends_on, produces):
    strike_index = pd.read_csv(depends_on, index_col=INDEX_COLS["strike_index"])
    strike_indicator = create_strike_indicator(strike_index, cutoff=1 / 3)
    strike_indicator.to_csv(produces)


for shoe_type in SHOE_TYPES:

    for data_set in DATA_SETS + ["tidy_ankle_moments", "strike_indicator"]:

        kwargs = {
            "produces": BLD.joinpath(f"data/{shoe_type}/{data_set}.csv"),
            "shoe_type": shoe_type,
            "data_set": data_set,
        }

        if data_set in {"tidy_ankle_moments", "strike_indicator"}:
            kwargs["depends_on"] = BLD.joinpath(f"data/{data_set}.csv")
        else:
            kwargs["depends_on"] = SRC.joinpath(f"data/{data_set}.csv")

        _id = f"{shoe_type}_{data_set}"

        @pytask.mark.task(id=_id, kwargs=kwargs)
        def task_filter_data(depends_on, produces, shoe_type, data_set):
            df = pd.read_csv(depends_on, index_col=INDEX_COLS[data_set])
            df_filtered = filter_by_shoe_type(df, shoe_type=shoe_type)
            df_filtered.to_csv(produces)
