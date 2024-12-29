import os
from mega import Mega
import re
import json

def sanitize_filename(filename: str, replacement: str = "_") -> str:

    # Define the characters to keep: alphanumeric, space, underscore, and dash
    valid_chars_pattern = r"[^a-zA-Z0-9 _\-\.]"
    
    # Replace invalid characters with the replacement string
    sanitized = re.sub(valid_chars_pattern, replacement, filename)
    
    # Replace sequences of replacement characters with a single replacement character
    sanitized = re.sub(f"{re.escape(replacement)}+", replacement, sanitized)
    
    # Strip leading and trailing replacement characters and spaces
    sanitized = sanitized.strip(f"{replacement} ")
    
    # Ensure it isn't empty after sanitization
    return sanitized if sanitized else "default_filename.pdf"

def download_link(link):
    mega = Mega()
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    try:
        m = mega.login(keys[0],keys[1])
    except Exception as e:
        print("Error download login failed.")
    try:
        m.download_url(link)
        return True
    except Exception as e:
        print("Error failed to download file.")
    return False

def get_all_pdf_links(start,end):

    mega = Mega()
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")

    try:
        m = mega.login(keys[0],keys[1])
        raise ValueError("Initial login sucessfull.. ")
    except Exception as e:
        print("Error Initial login failed.")


    all_files = m.get_files()
    files_lst = []
    count = 1
    for key,snippet in all_files.items():

        file_name = snippet['a']['n']
        if count<=end and snippet['p'] == 'PFICADKL' and ('.pdf' in file_name) and ('.crdownload' not in file_name):
            try:
                if count>=start:
                    link = m.export(file_name)

                    obj  = {
                        'link':link,
                        'file_name':file_name
                    }

                    files_lst.append(obj)
                count +=1
            except Exception as e:
                print("Error to get file Link.",e)

    return files_lst 
