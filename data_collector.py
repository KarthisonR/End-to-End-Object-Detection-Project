# import os
# import cv2
# import time
# import uuid

# IMAGE_PATH = "CollectedImages"

# labels = ["Car", "Pedestrian", "Bus", "Truck", "Motorcycle", "Bicycle", "auto", "van"]

# number_of_images = 100

# for label in labels:
#     img_path = os.path.join(IMAGE_PATH, label)
#     os.makedirs(img_path)

import requests
from bs4 import BeautifulSoup
import os

def download_images(query, num_images, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")
    
    count = 0
    for img in img_tags:
        img_url = img.get("src")
        try:
            img_response = requests.get(img_url)
            with open(os.path.join(save_folder, f"{query}_{count}.jpg"), "wb") as f:
                f.write(img_response.content)
            count += 1
            if count >= num_images:
                break
        except:
            pass

queries = ["car", "pedestrian", "bus", "truck", "motorcycle", "bicycle", "auto", "van"]
#queries = ["motorcycle on road"]
for query in queries:
    download_images(query, 100, f"./images/{query}")

    