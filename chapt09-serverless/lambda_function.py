"""
AWS Lambda function for hair type classification.

This function handles image classification using a TF-Lite model
to predict whether hair is straight or curly.
"""

import tflite_runtime.interpreter as tflite
import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image


# Model configuration
MODEL_NAME = "model_2024_hairstyle_v2.tflite"
TARGET_SIZE = (200, 200)

# Load the interpreter globally (cold start optimization)
interpreter = tflite.Interpreter(model_path=MODEL_NAME)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = input_details[0]['index']
output_index = output_details[0]['index']


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


def preprocess_input(url):
    """Download and preprocess image for inference"""
    # Download and prepare image
    img = download_image(url)
    img = prepare_image(img, TARGET_SIZE)

    # Convert to numpy array and normalize
    x = np.array(img, dtype='float32')
    x = x / 255.0  # Rescale to [0, 1]

    # Add batch dimension
    X = np.expand_dims(x, axis=0)

    return X


def predict(url):
    """Run prediction on image from URL"""
    # Preprocess input
    X = preprocess_input(url)

    # Set input tensor
    interpreter.set_tensor(input_index, X)

    # Run inference
    interpreter.invoke()

    # Get output
    preds = interpreter.get_tensor(output_index)

    return float(preds[0][0])


def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Expected event format:
    {
        "url": "https://example.com/image.jpg"
    }

    Returns:
    {
        "prediction": 0.693,
        "hair_type": "curly"
    }
    """
    try:
        # Get image URL from event
        url = event.get('url')

        if not url:
            return {
                'statusCode': 400,
                'body': {'error': 'Missing "url" parameter in request'}
            }

        # Run prediction
        prediction = predict(url)

        # Determine hair type
        # prediction > 0.5 means curly, <= 0.5 means straight
        hair_type = "curly" if prediction > 0.5 else "straight"

        return {
            'statusCode': 200,
            'body': {
                'prediction': prediction,
                'hair_type': hair_type
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': str(e)}
        }
