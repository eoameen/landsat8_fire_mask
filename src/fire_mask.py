import os
import argparse
import numpy as np
import rasterio
import logging
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def _validate_input(band_five: str, band_seven: str) -> bool:
    """validate input bands"""
    if not os.path.exists(band_five) or not os.path.exists(band_seven):
        raise ValueError('Make sure both input bands exists')
    return True


def generate_fire_mask(band_five: str, band_seven: str, out_dir: str) -> str:
    """generate binary fire mask"""
    # validate input
    _validate_input(band_five, band_seven)
    # calculate fire mask
    os.makedirs(out_dir, exist_ok=True)
    logger.info('calculating binary fire mask')
    np.seterr(divide='ignore')
    warnings.filterwarnings('ignore')
    mask_path = os.path.join(out_dir, 'binary_fire_mask.TIF')
    with rasterio.open(band_five) as ds5, rasterio.open(band_seven) as ds7:
        arr5, arr7 = ds5.read(), ds7.read()
        fire_mask = np.logical_and(
            np.greater(arr7, 0.5),
            np.logical_and(
                np.greater((arr7 - arr5), 0.3), np.greater((arr7 / arr5), 2.5)
            ),
        )
        fire_mask = fire_mask.astype(np.dtype(np.uint16))
        with rasterio.open(mask_path, "w", **ds5.profile) as dst:
            dst.write(fire_mask)
    return mask_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b5",
        "--band_five",
        help="path to band number 5",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-b7",
        "--band_seven",
        help="path to band number 7",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        help="Path to putput directory. Default is output/.",
        type=str,
        default="output",
    )
    args = parser.parse_args()
    generate_fire_mask(args.band_five, args.band_seven, args.output_directory)
