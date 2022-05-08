import os
from typing import Dict, Any

import numpy as np
from PIL import Image
NDArray = Any
Options = Any


def normalize_image(image: NDArray):
    """Normalize image pixels to be between [0., 1.0]"""
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    return normalized_image

def save_image(image, outdir: str):
    """A helper method that saves a dictionary of images"""

    def _prepare_to_save(prep_image: NDArray):
        """Helper method that converts the image to Uint8"""
        if prep_image.dtype == np.uint8:
            return image
        return normalize_image(prep_image).astype(np.uint8)

    if not os.path.exists(outdir):
        os.makedirs(outdir)


    Image.fromarray(_prepare_to_save(image)).save(f'{outdir}/output_image.png')
