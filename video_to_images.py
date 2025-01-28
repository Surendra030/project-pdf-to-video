import cv2
import os

import cv2
import os

def images_to_video(image_folder, output_video, fps=30):
    try:
        
        images = []
        for i in range(1,len(os.listdir(image_folder))+1):
            file_path = f'./{image_folder}/{i}_img.jpg'
            images.append(file_path)
        
        
        if not images:
            print("Error: No images found in the folder.")
            return
        
        # Read the first image to get the frame dimensions
        first_image_path = os.path.join(image_folder, images[0])
        frame = cv2.imread(first_image_path)
        height, width, layers = frame.shape

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        # Add each image to the video
        for image_name in images:
            img_path = os.path.join(image_folder, image_name)
            frame = cv2.imread(img_path)
            if frame is None:
                print(f"Warning: Could not read {image_name}, skipping.")
                continue
            video_writer.write(frame)

        # Release the video writer
        video_writer.release()
        print(f"Video created successfully: {output_video}")
        return output_video if os.path.exists(output_video) else None
    except Exception as e:
        print("Error:", e)



def video_to_images(video_file, output_folder):
    try:
            
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the video file
        video = cv2.VideoCapture(video_file)

        if not video.isOpened():
            print("Error: Could not open video.")
            return

        # Get the total number of frames in the video
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Iterate over all frames
        frame_count = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Increment frame count
            frame_count += 1

            # Save each frame as an image
            img_filename = f"{frame_count}_img.jpg"
            img_path = os.path.join(output_folder, img_filename)
            cv2.imwrite(img_path, frame)


        # Release the video capture object
        video.release()
        print("Video to images conversion completed!")
        return frame_count if os.path.exists(output_folder) else None
    except Exception as e:
        print("Error : ",e)

