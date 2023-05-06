import os
from bs4 import BeautifulSoup
import requests
import base64
import time

# user can input a topic and a number
# download first n images from google image search

GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

ROOT_FOLDER = "images"

def getBase64(img_data):
    head, data = img_data.split(',', 1)

    # Get the file extension (gif, jpeg, png)
    file_ext = head.split(';')[0].split('/')[1]

    # Decode the image data
    plain_data = base64.b64decode(data)
    return plain_data

def save_image(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)
    
def download_data():
    data = input("What images you want to download? ")
    num_imgs = int(input("Number of images to download? "))
    
    print("Start searching...")
    search_url = f"{GOOGLE_IMAGE}q={data}"
    print(search_url)
    
    res = requests.get(search_url, headers=usr_agent)
    html = res.content
    
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('img', {'class': 'rg_i'}, limit=num_imgs)
    print(results)
    
    img_links = []
    for result in results:
        base64Img = result['src']
        img_links.append(base64Img)
    with open('image_data.txt', 'w') as f:
        for base64Img in img_links:
            f.write(base64Img)
    
    print(f'found {len(img_links)} images')
    
    print("Start downloading...")
    
    SAVE_FOLDER = f"{ROOT_FOLDER}/{data}_{int(time.time())}"
    os.mkdir(SAVE_FOLDER)
    
    for i, imgString in enumerate(img_links):
        img_data = getBase64(imgString)
        # print(img_data)
        
        filename = f'{SAVE_FOLDER}/{data}_{i+1}.jpg'

        save_image(filename, img_data)
       

if __name__ == '__main__':
    if not os.path.exists(ROOT_FOLDER):
        os.mkdir(ROOT_FOLDER)
    download_data()