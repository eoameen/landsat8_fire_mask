import os
import pytest

from src.fire_mask import _validate_input, generate_fire_mask

# tests for _validate_input (Using valid input)
@pytest.mark.parametrize(
    "test_input",
    [
        # case 1
        {"band_five": "tests/data/LC08_L1TP_045033_20180811_20180811_01_RT/LC08_L1TP_045033_20180811_20180811_01_RT_B5.TIF",
        "band_seven": "tests/data/LC08_L1TP_045033_20180811_20180811_01_RT/LC08_L1TP_045033_20180811_20180811_01_RT_B7.TIF"},
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
        {"band_five": "tests/data/LC08_L1TP_045033_20180811_20180811_01_RT/LC08_L1TP_045033_20180811_20180811_01_RT_B5.TIF",
        "band_seven": "tests/data/LC08_L1TP_045033_20180811_20180811_01_RT/LC08_L1TP_045033_20180811_20180811_01_RT_B7.TIF",
        "output_directory": "output"},
    ],
)
def test_generate_fire_mask(test_input):
    mask_path = generate_fire_mask(
    test_input["band_five"],
    test_input["band_seven"],
    test_input["output_directory"]
    )
    assert os.path.exists(mask_path)
