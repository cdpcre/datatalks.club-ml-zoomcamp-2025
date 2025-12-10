from io import BytesIO
from urllib import request
from PIL import Image
import numpy as np

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
target_size = (200, 200)

img = download_image(url)
img_prep = prepare_image(img, target_size)

x = np.array(img_prep)
print("Raw shape:", x.shape)
print("Raw pixel at (0,0):", x[0, 0])
print("R channel:", x[0, 0, 0])
print("G channel:", x[0, 0, 1])
print("B channel:", x[0, 0, 2])
