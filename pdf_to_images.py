import fitz
import os

import cv2
import os
import numpy as np

import cv2
import os

def add_watermark_to_folder(folder_path):

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder {folder_path} not found!")
        return False

    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    if not image_files:
        print(f"No PNG images found in folder {folder_path}!")
        return False
    count = 1
    for index,image_file in enumerate(image_files,start=1):
        # Construct the full image path
        image_path = os.path.join(folder_path, image_file)

        # Extract the page number from the image name
        page_number = os.path.splitext(image_file)[0]  # Remove the '.png' extension

        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Unable to read the image {image_path}! Skipping...")
            continue


        # Get image dimensions
        height, width, _ = image.shape

        # Create a transparent overlay for the watermark
        overlay = image.copy()

        # watermark_text = page_number

        if count == 10:
            watermark_text = f"Subscribe to our channer : Time For Epics"
            count = 1
        else : watermark_text = page_number
        
        # Define font, scale, and color
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        font_thickness = 3
        color = (255, 0, 0)  # Blue text
        shadow_color = (0, 0, 0)  # Black shadow for better visibility
        opacity = 0.3


        # Calculate the size of the text box
        (text_width, text_height), baseline = cv2.getTextSize(watermark_text, font, font_scale, font_thickness)

        # Calculate the center position for the text
        x = (width - text_width) // 2
        y = (height + text_height) // 2

        # Add shadow to the overlay
        cv2.putText(overlay, watermark_text, (x + 2, y + 2), font, font_scale, shadow_color, font_thickness + 1, cv2.LINE_AA)

        # Add the watermark text to the overlay
        cv2.putText(overlay, watermark_text, (x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)

        # Blend the overlay with the original image
        watermarked_image = cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0)

        # Save the watermarked image to a temporary file
        temp_output_path = os.path.join(folder_path, f"temp_{image_file}")
        cv2.imwrite(temp_output_path, watermarked_image)

        # Remove the original image
        os.remove(image_path)

        # Rename the temporary file to the original image name
        os.rename(temp_output_path, image_path)
        count +=1

    print(f"Watermarking completed for all images in {folder_path}")
    return True




def pdf_to_images_with_fitz(pdf_path, output_folder='images', image_format="png"):
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)
        total_pages  = len(doc)
        # Iterate through each page
        for page_num in range(total_pages):
            page = doc[page_num]
            # Render page to a pixmap (image representation)
            pix = page.get_pixmap()
            
            # Define the output path
            image_path = f"{output_folder}/page_{page_num + 1}.{image_format}"
            
            # Save the pixmap as an image file
            pix.save(image_path)
            print(f"Saved: {image_path}")
        water_mark_added = add_watermark_to_folder(output_folder)
        print("All pages converted successfully.")


        if water_mark_added and  os.path.exists(output_folder) and total_pages > 0:

            os.remove(pdf_path)
            print("Sucessfully removed pdf file.")

        return total_pages
    except Exception as e:
        print(f"Error: {e}")

