import shutil
from mega import Mega
import os

import numpy as np

# np.set_printoptions(threshold=sys.maxsize)
import torch
from torchvision import transforms
from PIL import Image, ImageOps, ImageFilter

def convert_image_to_sketch(folder_name):
    images_lst = os.listdir(folder_name)
    for index,input_image_path in enumerate(images_lst):
        input_image_path = f'./{folder_name}/{index+1}_img.jpg'
        # Load image
        img = Image.open(input_image_path).convert('RGB')
        output_image_path = 'temp.png'
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
        os.remove(input_image_path)
        os.rename(output_image_path,input_image_path)


