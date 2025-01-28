import cv2
import os
import subprocess



def replace_audio(video_filename, audio_filename):
    """
    Replaces the audio in a video file with a new audio file, renames the output video,
    and deletes the original video.

    Args:
        video_filename (str): Path to the original video file.
        audio_filename (str): Path to the audio file to be added.

    Returns:
        str: The original video file name (with new content) if successful.
        bool: False if the process fails.
    """
    try:
        # Temporary output video file
        temp_video = "temp.mp4"

        # Command to replace audio in the video
        command = [
            "ffmpeg", "-i", video_filename, "-i", audio_filename,  # Input video and audio
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",  # Copy video, replace audio
            temp_video
        ]

        # Execute the FFmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Remove the original video file
        os.remove(video_filename)
        if os.path.exists(temp_video):
        # Rename temp video to the original video file name
            os.rename(temp_video, video_filename)

            return video_filename
        else: return None
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False



def extract_audio(filename, audio_filename):
    """
    Extracts audio from a video file using FFmpeg.
    
    Args:
        filename (str): Path to the input video file.
        audio_filename (str): Path for the output audio file (.mp3).
        
    Returns:
        str: The audio file name if created successfully.
        None: If the extraction process fails.
    """
    try:
        # Command to extract audio using FFmpeg
        command = [
            "ffmpeg", "-i", filename, "-vn",  # Input file and disable video stream
            "-acodec", "libmp3lame",  # Use MP3 codec
            audio_filename  # Output audio file
        ]
        
        # Execute the FFmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return audio_filename
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None


def images_to_video(image_folder, output_video, fps):
    try:
        print(f"Starting video creation from images in folder: '{image_folder}' with FPS: {fps}")
        images = []
        for i in range(1, len(os.listdir(image_folder)) + 1):
            file_path = f'./{image_folder}/{i}_img.jpg'
            if os.path.exists(file_path):
                images.append(file_path)
            else:
                print(f"Warning: File '{file_path}' does not exist, skipping.")

        if not images:
            print("Error: No valid images found in the folder. Exiting...")
            return None

        print(f"Found {len(images)} images. Preparing to create video...")
        
        # Read the first image to get the frame dimensions
        first_image_path = images[0]
        print(f"Reading the first image for dimensions: {first_image_path}")
        frame = cv2.imread(first_image_path)
        if frame is None:
            print("Error: Could not read the first image. Exiting...")
            return None
        
        height, width, layers = frame.shape
        print(f"Frame dimensions: Width={width}, Height={height}, Layers={layers}")

        # Initialize video writer
        print("Initializing video writer...")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        print(f"Video writer initialized with output file: {output_video}, FPS: {fps}")

        # Add each image to the video
        for idx, image_name in enumerate(images, start=1):
            img_path = image_name
            print(f"Processing image {idx}/{len(images)}: {img_path}")
            frame = cv2.imread(img_path)
            if frame is None:
                print(f"Warning: Could not read '{img_path}', skipping this image.")
                continue
            video_writer.write(frame)

        # Release the video writer
        video_writer.release()
        print(f"Video creation completed successfully: {output_video}")
        return output_video if os.path.exists(output_video) else None

    except Exception as e:
        print(f"Error during video creation: {e}")
        return None


def video_to_images(video_file, output_folder):
    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the video file
        video = cv2.VideoCapture(video_file)

        if not video.isOpened():
            print("Error: Could not open video.")
            return None, None

        # Get the total number of frames and FPS from the video
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        print(f"Original video FPS: {fps}")
        print(f"Total frames in original video: {total_frames}")

        # Iterate over all frames and save them as images
        frame_count = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Increment frame count and save frame as an image
            frame_count += 1
            img_filename = f"{frame_count}_img.jpg"
            img_path = os.path.join(output_folder, img_filename)
            cv2.imwrite(img_path, frame)

        # Release the video capture object
        video.release()
        print(f"Video to images conversion completed! {frame_count} images saved to '{output_folder}'")
        print(f"total img files  : {len(os.listdir(output_folder))}")
        # Return the total frame count and FPS
        return frame_count, fps
    except Exception as e:
        print(f"Error during video-to-images conversion: {e}")
        return None, None
