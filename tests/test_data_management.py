import numpy as np
import pandas as pd
import pytest
from functional_treatment_effects.data_management import create_indicator
from functional_treatment_effects.data_management import tidy_up_ankle_moments
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal


@pytest.mark.unit
def test_tidy_up_ankle_moments():
    df = pd.DataFrame({"a": [0, 1], "b": ["x", "y"], "5": [-1, -2]}).set_index(
        ["a", "b"]
    )
    got = tidy_up_ankle_moments(df)
    exp = pd.DataFrame(
        {"a": [0, 1], "b": ["x", "y"], "time": [5, 5], "moment": [-1, -2]}
    ).set_index(["a", "b", "time"])
    assert_frame_equal(got, exp)


@pytest.mark.unit
@pytest.mark.parametrize(
    "cutoff, exp", zip([1, -1, 2], [[0, 0, 1], [1, 1, 1], [0, 0, 0]])
)
def test_create_indicator(cutoff, exp):
    sr = pd.Series(np.arange(-1, 2))
    got = create_indicator(sr, cutoff=cutoff)
    assert_array_equal(got, exp)
