import onnxruntime as ort
import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

import os

model_path = os.getenv('MODEL_PATH', 'hair_classifier_v1.onnx')
if not os.path.exists(model_path):
    model_path = 'hair_classifier_empty.onnx'

session = ort.InferenceSession(model_path)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def predict(url):
    target_size = (200, 200)
    img = download_image(url)
    img_prep = prepare_image(img, target_size)
    
    x = np.array(img_prep, dtype='float32')
    x /= 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype='float32')
    std = np.array([0.229, 0.224, 0.225], dtype='float32')
    x = (x - mean) / std
    x = np.transpose(x, (2, 0, 1))
    X = np.array([x])
    
    pred = session.run([output_name], {input_name: X})[0]
    return float(pred[0][0])

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result
