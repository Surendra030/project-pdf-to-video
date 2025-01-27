from mega import Mega
import json
import os

keys = 'afg154006@gmail.com_megaMac02335!'.split("_")
mega = Mega()

try:
        
    m = mega.login(keys[0],keys[1])
except Exception as e:
    print("Error failed to login..")
    
all_files = m.get_files().items()
with open('temp.json')as f:
    data = json.load(f)
    
try:
    index = 1
    for key,snippet in all_files:
        print(f"{index}/{len(all_files)}")
        index +=1
        file_name = snippet['a']['n']
        if '.mp4' in file_name and 'sxoE2SRI' in snippet['p']:
                
            for obj in data:
                try:
                    old_name=  str(obj['old']).replace('.pdf','.mp4')
                    new_name = str(obj['new']).replace('.pdf','.mp4')

                    if file_name == old_name:
                        file = m.find(old_name)
                        m.rename(file,new_name)
                        
                except Exception as e:
                    print("Error failed to rename :",e)
                    
except Exception as e:
    print("Error failed to loop : ",e)

all_files_new =m.get_files().items()

final_data = []

for key,snippet in all_files_new:
    file_name = snippet['a']['n']
    if '.mp4' in file_name:
        link = m.export(file_name)
        obj = {
            'fileName':file_name,
            'link':link
        }
        final_data.append(obj)

fs = 'links_data_video.json'
with open(fs,'w',encoding='utf-8')as f:
    json.dump(final_data,f,indent=4)
    
try:
    m.upload(fs)
    
except Exception as e:
    print("Error failed to upload :",e)