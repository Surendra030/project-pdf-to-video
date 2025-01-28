import cv2
import sys
from mega import Mega
import os
import shutil
import cv2 as cv

from video_to_images import replace_audio, video_to_images,images_to_video,extract_audio

def convert_to_sketch(input_image, output_image, darkness_factor=0.7):
    """
    Convert an image to a pencil sketch with adjustable darkness.
    
    Parameters:
        input_image (str): Path to the input image.
        output_image (str): Path to save the output sketch.
        darkness_factor (float): Multiplier to control the darkness of the sketch. Default is 1.0.
    """
    
    try:
        if os.path.exists(input_image) or os.path.exists('file.jpg'):
            input_image = 'file.jpg'
            print(f"{input_image} file exits...")
                
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


def temp(folder_name):
    
    
    img_files = os.listdir(folder_name)
    
    try:
        print(len(img_files))
        for index,file in enumerate(img_files,start=1):
            file = f'./{folder_name}/{index}_img.jpg'
            
            if index >= len(img_files)+1:
                print("stopped index num :",index)
                return True
            if not os.path.exists(file): return len(img_files)

            # Replace this image name to your image name
            image = cv.imread(file)

            # Converting the Image into gray_image
            gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            # Inverting the Imge
            invert_image = cv.bitwise_not(gray_image)

            # Blur Image
            blur_image = cv.GaussianBlur(invert_image, (21,21), 0)

            # Inverting the Blured Image
            invert_blur = cv.bitwise_not(blur_image)

            # Convert Image Into sketch
            sketch = cv.divide(gray_image, invert_blur, scale=250.0)
            temp_name = 'tempimg.jpg'
            
            cv.imwrite(temp_name, sketch)
            
            if os.path.exists(temp_name):
                
                os.rename(temp_name,file)
                print("file renamed sucessfully...")
        return True
    except Exception as e:
        print("Error : ",e)
        
        
    
if __name__ == "__main__":
    
    keys = 'afg154006@gmail.com_megaMac02335!'.split("_")
    mega = Mega()
    m = mega.login(keys[0],keys[1])
    m.download_url("https://mega.nz/file/ivJTRJBa#PfD03_lWQLZPkNKCjO1ttoV_odB60dYLaDgIwPrOAjs")
    
    file_name = [f for f in os.listdir() if '.mp4' in f]
    file_name = os.rename(file_name[0],'file.mkv')
    file_name = 'file.mkv'
    audio_file = 'audio_file.mp3'
    if os.path.exists(file_name):
        print(f"File {file_name} exists. Proceeding with processing...")
        folder_name = "images"
        frame_count, fps = video_to_images(file_name, folder_name)
        
        if frame_count is not None and fps is not None:

            print(f"Images successfully extracted to folder '{folder_name}'. Proceeding to sketch transformation...")
            sketch_flag = temp(folder_name)
            
            if True:
                print("Sketch transformation completed. Proceeding to create video from images...")
                
                zip_file = 'temp_output_video.mp4'
                output_file_name = images_to_video(folder_name, zip_file, fps=fps)
                result = extract_audio(file_name, audio_file)
                
                if os.path.exists(audio_file):
                    output_file_name = replace_audio(output_file_name,audio_file)
                    
                
                
                if output_file_name and os.path.exists(output_file_name):
                    print(f"Video created successfully: {output_file_name}")
                    keys = 'afg154006@gmail.com_megaMac02335!'.split("_")
                    mega = Mega()
                    
                    try:
                        print("Logging into Mega account...")
                        m = mega.login(keys[0], keys[1])
                        print("Upload initiated to Mega...")
                        m.upload(output_file_name)
                        print(f"Upload successful: {output_file_name}")
                        
                        print(f"Cleaning up by removing folder '{folder_name}' and file '{file_name}'...")
                        shutil.rmtree(folder_name)
                        os.remove(file_name)
                        
                    except Exception as e:
                        print(f"Error: Failed to upload. Exception: {e}")
                else:
                    print(f"Error: Output video '{output_file_name}' does not exist.")
            else:
                print("Error: Sketch transformation failed.")
        else:
            print(f"Error: Failed to extract images from video '{file_name}'.")
    else:
        print(f"Error: File '{file_name}' does not exist. Current directory contents: {os.listdir()}")

    # input_image = 'flle.jpg'
    # output_image = 'file1.png'
    # convert_to_sketch(input_image, output_image)
    # temp()
    
    # if os.path.exists(output_image):
    #     keys = 'afg154006@gmail.com_megaMac02335!'.split("_")
    #     mega = Mega()
    #     m = mega.login(keys[0],keys[1])
    #     try:
    #         m.upload(output_image)
    #     except Exception as e:
    #         print("Error failed to upload : ")
    # else:
    #     print("img not found..")