from pdf_to_images import pdf_to_images_with_fitz
from image_to_video import create_video_with_watermark
from get_pdf_links import get_all_pdf_links, download_link

import os
import json

from mega import Mega

start = 1
end  = 3

 
all_pdf_files = get_all_pdf_links(start,end)



if all_pdf_files:
    print("\n Pdf file links are not Empty..")
    data = all_pdf_files
    for index,pdf_obj in enumerate(data):
        print(f'{index} - {len(data)}')
        pdf_path = pdf_obj['file_name']
        link = pdf_obj['link']
        file_present_flag = download_link(link)

        if file_present_flag:
            total_pages = pdf_to_images_with_fitz(pdf_path)

            if total_pages:
                
                print("\npdf to images converted sucessflly..")
                video_path = create_video_with_watermark(pdf_path,total_pages=total_pages)
                print("\npdf to video converted sucessfully..")
                if os.path.exists(video_path):
                    keys = os.getenv("M_TOKEN")
                    keys = keys.split("_")


                    mega = Mega()
                    flag = False
                    try:
                        m = mega.login(keys[0],keys[1])
                        print("login sucessfull..")
                    except Exception as e:
                        print("login failed..")



                    try:
                        
                        m.upload(video_path,dest='OdhCgTJR')
                        
                        print("video uploded sucessfully...")
                    except Exception as e:
                        print("Error failed to upload : ",e)

                    finally:
                        os.remove(video_path)
                        print("Sucessfully removed video file.")
                        

        else: print("pdf to images convertion failed..")

else:
    print("Pdf files list is Empty.",all_pdf_files)
