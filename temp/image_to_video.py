import random
import shutil
import os

from moviepy.editor import ImageSequenceClip, ImageClip, CompositeVideoClip
import cv2

from get_pdf_links import sanitize_filename



def resize_images_to_first_image_size(image_folder):
    # Get the list of image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    if not image_files:
        print("No image files found in the folder.")
        return []

    # Load the first image to get its size
    first_image_path = os.path.join(image_folder, image_files[0])
    first_img = cv2.imread(first_image_path)
    
    # Check if the first image was loaded correctly
    if first_img is None:
        print(f"Error loading image: {first_image_path}")
        return []

    # Get the width and height of the first image
    height, width = first_img.shape[:2]
    
    # List to store the paths of the resized images
    resized_image_paths = []
    # Loop through all the images and resize them to the first image's size
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"Error loading image: {image_path}")
            continue
        
        # Resize the image
        resized_img = cv2.resize(img, (width, height))

        # Save the resized image with a temporary name
        temp_image_path = os.path.join(image_folder, f"temp_{image_file}")
        cv2.imwrite(temp_image_path, resized_img)

        # Remove the original image (optional step)
        os.remove(image_path)

        # Rename the resized image to the original name
        os.rename(temp_image_path, image_path)

        # Add the path of the resized image to the list
        resized_image_paths.append(image_path)
    print(resized_image_paths)
    # Return the list of resized image paths
    return resized_image_paths




def create_video_with_watermark(video_output_path, total_pages, image_folder='images', logo_path='logo.png'):
    video_output_path = sanitize_filename(video_output_path)
    # Ensure the output video has the correct extension
    video_output_path = f"{str(video_output_path).split('.pdf')[0]}.mp4"

    # Prepare the list of image files
    image_files = resize_images_to_first_image_size(image_folder)
    
    image_files = [f'{image_folder}/page_{i}.png' for i in range(1, total_pages + 1)]


    # Check if the image files exist
    for img in image_files:
        if not os.path.exists(img):
            raise FileNotFoundError(f"Image not found: {img}")

    # Set durations for each image fps = (1/seconds) (1/5seconds) = 0.2fps

    # Create a video clip from the images with specified durations
    clip = ImageSequenceClip(image_files,fps=0.2)

    # Get the video dimensions (width, height)
    # video_width, video_height = clip.size

    # # Define the function to calculate random positions
    # def random_position(t):
        
    #     # Change position only at the start of every second
    #     random.seed(1)  # Use time (t) as seed for consistency
    #     x = random.randint(0, video_width - logo.w)  # Ensure logo stays within video bounds
    #     y = random.randint(0, video_height - logo.h)
    #     return (x, y)

    # # Load the logo image and configure it
    # logo = ImageClip(logo_path).set_duration(clip.duration).resize(height=70)

    # # Animate the logo to appear at a random position every second
    # logo = logo.set_position(random_position)

    # # Combine the main video with the watermark (logo)
    # final_clip = CompositeVideoClip([clip, logo])
    # Write the final video to the specified output path
    
    clip.write_videofile(video_output_path, codec='libx264')


    # Check if the video was created successfully
    if os.path.exists(video_output_path):
        shutil.rmtree(image_folder)
        print(f"Sucessfully removed {image_folder} folder.")

        return video_output_path
    else:
        return None

