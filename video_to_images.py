import cv2
import os

import cv2
import os


import cv2
import os
import subprocess


def images_to_video(audio_file,image_folder, output_video, fps):
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

        # Calculate and print the new video length
        video_length = len(images) / fps
        print(f"New video length: {video_length:.2f} seconds")

        # If audio file is provided, merge it with the video
        if audio_file:
            print("Merging audio into the video...")
            final_output = output_video.replace(".mp4", "_with_audio.mp4")
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",  # Overwrite output file if it exists
                "-i", output_video,  # Input video
                "-i", audio_file,  # Input audio
                "-c:v", "copy",  # Copy video codec
                "-c:a", "aac",  # Encode audio with AAC
                "-map", "0:v:0",  # Use video stream from the first input
                "-map", "1:a:0",  # Use audio stream from the second input
                final_output
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"Audio merged successfully! Final video: {final_output}")
            return final_output if os.path.exists(final_output) else None

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

        # Calculate the original video length
        video_length = total_frames / fps
        print(f"Original video length: {video_length:.2f} seconds")
        print(f"Original video FPS: {fps}")
        print(f"Total frames in original video: {total_frames}")

        # Extract audio from the video
        audio_file = video_file.replace(".mp4", ".aac")
        print("Extracting audio from the original video...")
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-i", video_file,  # Input video
            "-vn",  # No video
            "-acodec", "copy",  # Copy audio codec
            audio_file
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Audio extracted successfully: {audio_file}")

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
        print(f"Total image files: {len(os.listdir(output_folder))}")

        # Return the total frame count, FPS, and audio file path
        return frame_count, fps, audio_file
    except Exception as e:
        print(f"Error during video-to-images conversion: {e}")
        return None, None, None
