import numpy as np
import pandas as pd


# ======================================================================================
# Data set information
# ======================================================================================

DATA_SETS = ["ankle_moments", "strike_index", "subject_information"]

INDEX_COLS = {
    "ankle_moments": ["shoe_type", "variable", "id"],
    "strike_index": ["shoe_type", "id"],
    "subject_information": ["id"],
    "tidy_ankle_moments": ["shoe_type", "variable", "id", "time"],
    "strike_indicator": ["shoe_type", "id"],
}

SHOE_TYPES = ["adrenaline", "bare", "beast", "glycerin"]


# ======================================================================================
# Data management functions
# ======================================================================================


def tidy_up_ankle_moments(df: pd.DataFrame):
    """Create tidy (long) version of ankle moments data.

    Args:
        df (pd.DataFrame): The ankle moments data.

    Returns:
        pd.DataFrame: The data in a tidy (long) format, with multiindex (shoe_type,
            variable, id, time).

    """
    tidy = df.melt(var_name="time", value_name="moment", ignore_index=False)
    tidy["time"] = tidy["time"].astype(np.int64)
    tidy = tidy.set_index("time", append=True)
    tidy = tidy.sort_index()
    return tidy


def create_indicator(sr: pd.Series, *, cutoff: float):
    """Create indicator from float series.

    Args:
        sr (pd.Series): Series containing float values.
        cutoff (float): Cutoff value. All values in sr above or equal to cutoff will be
            converted to a 1, all values below to 0.

    Returns:
        pd.Series: The indicator series.

    """
    indicator = (sr >= cutoff).astype(np.int64)
    return indicator
