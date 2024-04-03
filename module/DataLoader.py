import requests
import sys, os
from PIL import Image
import json
import io
import numpy as np
import matplotlib.pyplot as plt
import skimage

sys.path.append(os.pardir)

def loadImg(lat, lon, APIkey):
    endpoint = 'https://maps.googleapis.com/maps/api/streetview/metadata'

    location = f'{lat},{lon}'
    image_container = []
    for i in range(4):
        heading = i*90
        params = {
            'location': location,
            'key': APIkey,
            'heading': f"{heading}",
        }
        url = f"https://maps.googleapis.com/maps/api/streetview?size=640x192&location={params['location']}&heading={params['heading']}&key={params['key']}"

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        bytes_data = response.content
        image_parts = Image.open(io.BytesIO(bytes_data))
        image_parts = np.array(image_parts) # 320, 256, 3

        image_container.append(image_parts)
        r = requests.get(endpoint, params=params)
        panoID = r.json()['pano_id']

    # Concatenate 4 images
    # image = np.concatenate((image_container[0], image_container[1], image_container[2], image_container[3]), axis=1)
    image = image_container[0]

    return image, panoID

def loadLocalImg(path):
    imageOriginal = skimage.io.imread(path)
    image = skimage.transform.resize(imageOriginal, (320, 1024))
    image = image[:, :, :3]
    image = skimage.img_as_ubyte(image)
    return image