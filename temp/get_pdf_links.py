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
    keys = 'afg154006@gmail.com_megaMac02335!'.split("_")
    try:
        m = mega.login(keys[0],keys[1])
    except Exception as e:
        print("Error download login failed.")
    try:
        m.download_url(link)
        return True
    except Exception as e:
        print("Error failed to download file.",e)
    return False

def get_all_pdf_links(start,end):

    mega = Mega()
    keys = os.getenv("M_TOKEN")
    keys = 'afg154006@gmail.com_megaMac02335!'.split("_")

    try:
        m = mega.login(keys[0],keys[1])
    except Exception as e:
        print("Error Initial login failed.",e)


    try:
        f="pdf_links_data.json"
        link = m.export("pdf_links_data.json") 
        m.download_url(link) 
        if os.path.exits(f):
            with open(f,encoding='utf-8')as f :
                data = json.load(f)
                f.close()
                return data if len(data) > 0 else m.getfiles() 
                

    except Exception as e:
        print("error :",) 
            
