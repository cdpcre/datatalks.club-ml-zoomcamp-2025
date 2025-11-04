#!/usr/bin/env python3
"""
Question 1: Convert Keras model to TF-Lite format and check size.

This script downloads the Keras model and converts it to TF-Lite format.
"""

import tensorflow as tf
from tensorflow import keras
import os
from urllib import request


def download_model(url, path):
    """Download model if it doesn't exist"""
    if not os.path.exists(path):
        print(f"Downloading model from {url}...")
        request.urlretrieve(url, path)
        print(f"Model downloaded to {path}")
    else:
        print(f"Model already exists at {path}")
    return path


def convert_to_tflite(keras_model_path, tflite_model_path):
    """Convert Keras model to TF-Lite format"""
    # Load the Keras model
    print(f"Loading Keras model from {keras_model_path}...")
    model = keras.models.load_model(keras_model_path)
    print(f"Model loaded successfully")
    print(f"Input shape: {model.input_shape}")
    print(f"Output shape: {model.output_shape}")

    # Convert to TF-Lite
    print(f"\nConverting to TF-Lite format...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the TF-Lite model
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)

    # Get the file size
    file_size_bytes = os.path.getsize(tflite_model_path)
    file_size_mb = file_size_bytes / (1024 * 1024)

    print(f"\nTF-Lite model saved to {tflite_model_path}")
    print(f"File size: {file_size_bytes:,} bytes")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"\n{'='*50}")
    print(f"✓ ANSWER Q1: {round(file_size_mb)} Mb")
    print(f"{'='*50}")

    return tflite_model_path, file_size_mb


def main():
    # Configuration
    model_url = "https://github.com/alexeygrigorev/large-datasets/releases/download/hairstyle/model_2024_hairstyle.keras"
    keras_model_path = "model_2024_hairstyle.keras"
    tflite_model_path = "model_2024_hairstyle.tflite"

    # Download model
    download_model(model_url, keras_model_path)

    # Convert to TF-Lite
    convert_to_tflite(keras_model_path, tflite_model_path)


if __name__ == "__main__":
    main()
