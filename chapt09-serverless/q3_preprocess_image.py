#!/usr/bin/env python3
"""
Question 3: Preprocess test image and get first pixel R channel value.

This script downloads and preprocesses the test image, then checks the
R channel value of the first pixel.
"""

import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image


def download_image(url):
    """Download an image from a URL"""
    print(f"Downloading image from {url}...")
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    print(f"Image downloaded: size={img.size}, mode={img.mode}")
    return img


def prepare_image(img, target_size):
    """Prepare image for model input"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_image(url, target_size=(200, 200)):
    """Download and preprocess image for inference"""
    # Download image
    img = download_image(url)

    # Prepare image
    print(f"\nPreparing image with target size {target_size}...")
    img_prepared = prepare_image(img, target_size)
    print(f"Prepared image size: {img_prepared.size}")

    # Convert to numpy array
    x = np.array(img_prepared, dtype='float32')
    print(f"Array shape: {x.shape}")
    print(f"Array dtype: {x.dtype}")
    print(f"Array value range: [{x.min():.1f}, {x.max():.1f}]")

    # Preprocess: rescale to [0, 1] (as done in homework 8)
    x = x / 255.0
    print(f"After rescaling: [{x.min():.3f}, {x.max():.3f}]")

    # Get the first pixel, R channel value
    first_pixel_r = x[0, 0, 0]
    first_pixel_g = x[0, 0, 1]
    first_pixel_b = x[0, 0, 2]

    print("\n" + "="*50)
    print("FIRST PIXEL VALUES:")
    print("="*50)
    print(f"  R (Red):   {first_pixel_r:.4f}")
    print(f"  G (Green): {first_pixel_g:.4f}")
    print(f"  B (Blue):  {first_pixel_b:.4f}")
    print("\n" + "="*50)
    print(f"✓ ANSWER Q3: {first_pixel_r:.2f}")
    print("="*50)

    return x, first_pixel_r


def main():
    test_image_url = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
    target_size = (200, 200)  # From homework 8

    preprocess_image(test_image_url, target_size)


if __name__ == "__main__":
    main()
