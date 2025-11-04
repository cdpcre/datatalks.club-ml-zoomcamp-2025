#!/usr/bin/env python3
"""
Question 4: Run inference on test image using TF-Lite model.

This script applies the TF-Lite model to the preprocessed test image.
"""

import tensorflow as tf
import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image


def download_image(url):
    """Download an image from a URL"""
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    """Prepare image for model input"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_image(url, target_size=(200, 200)):
    """Download and preprocess image for inference"""
    img = download_image(url)
    img_prepared = prepare_image(img, target_size)
    x = np.array(img_prepared, dtype='float32')
    x = x / 255.0  # Rescale to [0, 1]
    return x


def run_inference(tflite_model_path, image_array):
    """Run inference using TF-Lite model"""
    print(f"Loading TF-Lite model from {tflite_model_path}...")

    # Load the TF-Lite model
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Add batch dimension
    X = np.expand_dims(image_array, axis=0)
    print(f"Input shape with batch dimension: {X.shape}")

    # Set the input tensor
    input_index = input_details[0]['index']
    interpreter.set_tensor(input_index, X)

    # Run inference
    print("Running inference...")
    interpreter.invoke()

    # Get the output
    output_index = output_details[0]['index']
    preds = interpreter.get_tensor(output_index)

    print(f"Output shape: {preds.shape}")
    print(f"Prediction value: {preds[0][0]:.3f}")

    print("\n" + "="*50)
    print(f"✓ ANSWER Q4: {preds[0][0]:.3f}")
    print("="*50)

    return preds[0][0]


def main():
    # Configuration
    tflite_model_path = "model_2024_hairstyle.tflite"
    test_image_url = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
    target_size = (200, 200)  # From homework 8

    # Preprocess image
    print("Preprocessing image...")
    x = preprocess_image(test_image_url, target_size)

    # Run inference
    prediction = run_inference(tflite_model_path, x)

    # Interpret result
    print(f"\nInterpretation:")
    if prediction > 0.5:
        print(f"  Prediction: CURLY (confidence: {prediction:.3f})")
    else:
        print(f"  Prediction: STRAIGHT (confidence: {1-prediction:.3f})")


if __name__ == "__main__":
    main()
