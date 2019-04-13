import os
import re
import subprocess
from urllib import request
import shutil


directory = "/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/other_html"

for filename in os.listdir(directory):
    new_name = os.path.join(directory, filename.replace('.', '_') + '.html')
    os.rename(os.path.join(directory, filename), new_name)
    '''
        if re.search('=(.*)&Lang', filename):
        new_filename = re.search('=(.*)&Lang', filename).group(1).replace('%2F', '_') + '.doc'
        print(new_filename)
        os.rename(filename, new_filename)

    # Files with + in their filenames
    
    if "+" in filename:
        #new_filename = filename.replace('+', '').replace('_', '/').replace('.doc', '')
        #download_link = f"https://daccess-ods.un.org/access.nsf/GetFile?Open&DS={new_filename}&Lang=E&Type=DOC"
        #print(download_link)
        #download_file(download_link, new_filename)
        #subprocess.call(['wget', download_link, '-P  images/'])
    # move files    
    #shutil.move(path, target)
    '''



