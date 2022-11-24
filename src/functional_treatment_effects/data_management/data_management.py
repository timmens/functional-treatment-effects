import numpy as np
import pandas as pd


DATA_SETS = ["ankle_moments", "strike_index", "subject_information"]
INDEX_COLS = {
    "ankle_moments": ["shoe_type", "variable", "id"],
    "strike_index": ["shoe_type", "id"],
    "subject_information": ["id"],
    "tidy_ankle_moments": ["shoe_type", "variable", "id"],
    "strike_indicator": ["shoe_type", "id"],
}

SHOE_TYPES = ["adrenaline", "bare", "beast", "glycerin"]


def filter_by_shoe_type(df, shoe_type=None):
    if shoe_type is None:
        raise ValueError(f"shoe_type needs to be in {SHOE_TYPES}.")

    if "shoe_type" in df.index.names:
        df = df.query("shoe_type == @shoe_type")
        df = df.droplevel("shoe_type", axis=0)

    return df


def create_tidy_ankle_moments(df):
    tidy = df.reset_index()
    tidy = tidy.melt(
        id_vars=["shoe_type", "variable", "id"], var_name="time", value_name="moment"
    )
    tidy["time"] = tidy["time"].astype(np.int64)
    tidy = tidy.set_index(["shoe_type", "variable", "id", "time"])
    tidy = tidy.sort_index()
    return tidy


def create_strike_indicator(strike_index: pd.DataFrame, *, cutoff: float):
    strike_indicator = (strike_index >= cutoff).astype(np.int64)
    strike_indicator = strike_indicator.rename(
        columns={"strike_index": "strike_indicator"}
    )
    return strike_indicator
