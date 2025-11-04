#!/usr/bin/env python3
"""
Question 2: Get the output index for the TF-Lite model.

This script inspects the TF-Lite model to find input/output tensor indices.
"""

import tensorflow as tf


def get_model_info(tflite_model_path):
    """Get input and output details from TF-Lite model"""
    # Load the TF-Lite model
    print(f"Loading TF-Lite model from {tflite_model_path}...")
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print("\n" + "="*50)
    print("INPUT DETAILS:")
    print("="*50)
    for detail in input_details:
        print(f"  Index: {detail['index']}")
        print(f"  Name: {detail['name']}")
        print(f"  Shape: {detail['shape']}")
        print(f"  Type: {detail['dtype']}")

    print("\n" + "="*50)
    print("OUTPUT DETAILS:")
    print("="*50)
    for detail in output_details:
        print(f"  Index: {detail['index']}")
        print(f"  Name: {detail['name']}")
        print(f"  Shape: {detail['shape']}")
        print(f"  Type: {detail['dtype']}")

    output_index = output_details[0]['index']
    print("\n" + "="*50)
    print(f"✓ ANSWER Q2: {output_index}")
    print("="*50)

    return input_details, output_details


def main():
    tflite_model_path = "model_2024_hairstyle.tflite"
    get_model_info(tflite_model_path)


if __name__ == "__main__":
    main()
