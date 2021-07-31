import os
import pytest

from conftest import BAND_FIVE, BAND_SEVEN

from src.fire_mask import _validate_input, generate_fire_mask

# tests for _validate_input (Using valid input)
@pytest.mark.parametrize(
    "test_input",
    [
        # case 1
        {"band_five": BAND_FIVE,
        "band_seven": BAND_SEVEN},
    ],
)
def test_validate_input_by_valid_input(test_input):
    assert _validate_input(**test_input)


# tests for _validate_input (Using invalid input)
@pytest.mark.parametrize(
    "test_input",
    [
        # case 1
        {"band_five": "tests/B5.TIF",
        "band_seven": "tests/B7.TIF"},
    ],
)
def test_validate_input_by_invalid_input(test_input):
    with pytest.raises(ValueError):
        _validate_input(**test_input)


# tests for generate_fire_mask
@pytest.mark.parametrize(
    "test_input",
    [
        # case 1
        {"band_five": BAND_FIVE,
        "band_seven": BAND_SEVEN},
    ],
)
def test_generate_fire_mask(test_input, tmpdir):
    mask_path = generate_fire_mask(
    test_input["band_five"],
    test_input["band_seven"],
    tmpdir
    )
    assert os.path.exists(mask_path)
