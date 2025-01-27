import cv2
import os

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

