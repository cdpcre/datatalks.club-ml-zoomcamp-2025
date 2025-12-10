from io import BytesIO
from urllib import request

import numpy as np
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

url = 'https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'
target_size = (200, 200) # Based on Q2 expectation, will verify with q2 output

img = download_image(url)
img_prep = prepare_image(img, target_size)

x = np.array(img_prep, dtype='float32')
x /= 255.0
mean = np.array([0.485, 0.456, 0.406], dtype='float32')
std = np.array([0.229, 0.224, 0.225], dtype='float32')
x = (x - mean) / std
X = np.array([x])

print("First pixel R channel value:", X[0, 0, 0, 0])
