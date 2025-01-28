from sketchify import sketch
import os

def convert_image_to_sketch(input_image_path, output_folder, output_image_name):
    try:
        # Call sketchify's normal sketch method
        sketch.normalsketch(input_image_path, output_folder, output_image_name)
        print(f"Sketch saved successfully as {output_folder}/{output_image_name}.png")
        return True
    except Exception as e:
        print(f"Error processing image {input_image_path}: {e}")
        return False

def convert_to_sketch(folder_name):
    images_lst = os.listdir(folder_name)
    if not images_lst:
        print("No images found in the folder.")
        return False
        
    for index, input_image_name in enumerate(images_lst):
        input_image_path = f"./{folder_name}/{input_image_name}"
        
        # Check if the file is an image (optional check)
        if not input_image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Skipping non-image file: {input_image_name}")
            continue
        
        output_folder = folder_name  # Output folder is the same as the input folder
        output_image_name = f"temp_{index + 1}"  # Temporary name for the output image
        
        # Process the image and convert it to a sketch
        result = convert_image_to_sketch(input_image_path, output_folder, output_image_name)
        
        if result:
            try:
                # Remove the original image after processing
                os.remove(input_image_path)
                print(f"Original image {input_image_name} deleted.")
                
                # Rename the temporary sketch file to the original image's name
                temp_image_path = f"{output_folder}/{output_image_name}.png"
                os.rename(temp_image_path, f"{folder_name}/{input_image_name}")
                print(f"Sketch renamed to {folder_name}/{input_image_name}")
            
            except Exception as e:
                print(f"Error deleting or renaming files: {e}")
                return False

    print("All images processed successfully.")
    return True
