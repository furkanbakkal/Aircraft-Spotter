## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import requests
import json
import pandas as pd
import time
from bs4 import BeautifulSoup

#go to  https://jetphotos.com get photo and download it
def save_image(reg_data):
# Set up the image URL and filename
    try:
        url_data="https://jetphotos.com/photo/keyword/"+reg_data 
        response=requests.get(url_data).text
        soup=BeautifulSoup(response,"html.parser")
        soup=soup.find_all("img",class_="result__photo")
        img=str(soup[2])
        img=img.split('"')
        url=img[7].split("//")
        image_url="https://"+url[1]
        #print(image_url)

        filename = "plane.png"

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
            print('Image sucessfully Downloaded')
            return True
        else:
            print('Image Couldn\'t be retreived')
            return False

    except IndexError:
        print("There is no image for: #"+str(reg_data)+ " , will not send Message")
        return False