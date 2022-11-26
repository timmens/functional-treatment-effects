import numpy as np
import pandas as pd
import pytest
from functional_treatment_effects.data_management import create_strike_indicator
from numpy.testing import assert_array_equal


def test_filter_by_shoe_type():
    pass


def test_create_tidy_ankle_moments():
    pass


@pytest.mark.unit
def test_create_strike_indicator():
    strike_index = pd.DataFrame(
        {"strike_index": np.arange(-1, 2), "id": [0, 1, 2]}
    ).set_index("id")
    got = create_strike_indicator(strike_index, cutoff=1)
    expected = pd.DataFrame(
        {"strike_indicator": [0, 0, 1], "id": [0, 1, 2]}, dtype=np.int64
    ).set_index("id")
    assert_array_equal(got, expected)
