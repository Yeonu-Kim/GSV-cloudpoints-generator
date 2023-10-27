import requests
import sys, os
from PIL import Image
import json
import io
import numpy as np

sys.path.append(os.pardir)
from util.Encode import parse, parseHeader, parsePlanes, get_bin, getFloat32, getUInt16, bin_to_float, computeDepthMap

def loadImg(lat, lon, APIkey):
    endpoint = 'https://maps.googleapis.com/maps/api/streetview/metadata'

    location = f'{lat},{lon}'
    params = {
        'location': location,
        'key': APIkey,
    }

    url = f"https://maps.googleapis.com/maps/api/streetview?size=400x300&location={params['location']}&key={params['key']}"

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    bytes_data = response.content
    image = Image.open(io.BytesIO(bytes_data))

    r = requests.get(endpoint, params=params)
    panoID = r.json()['pano_id']
    print(panoID)

    return image, panoID

def loadDepth(panoID):
    # Set API endpoint URL
    endpoint = 'https://www.google.com/maps/photometa/v1'

    # https://www.google.co.kr/maps/@/data=!3m6!1e1!3m4!1s8ZzNUOYHXzacRZS_rlBewg!2e0!7i13312!8i6656?hl=ko&entry=ttu
    # https://www.google.co.kr/maps/@/data=!3m6!1e1!3m4!1sruGrZNOzKF9tupB528vxCQ!2e0!7i13312!8i6656?hl=ko&entry=ttu
    # https://www.google.co.kr/maps/dir/37.281575,127.0017723/%EA%B2%BD%EA%B8%B0%EB%8F%84+%EC%88%98%EC%9B%90%EC%8B%9C/data=!3m1!4b1!4m8!4m7!1m0!1m5!1m1!1s0x357b430a20764611:0xf1373002ee5db4c9!2m2!1d127.0077847!2d37.2803896?hl=ko&entry=ttu
    # <iframe src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d793.6430016539113!2d127.00112856961431!3d37.28157499825712!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMzfCsDE2JzUzLjciTiAxMjfCsDAwJzA2LjQiRQ!5e0!3m2!1sko!2skr!4v1696575796810!5m2!1sko!2skr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    # !3m7!1e1!3m5!1sfxezu1hF3ARauW5Yva2VqA!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fpanoid%3Dfxezu1hF3ARauW5Yva2VqA%26cb_client%3Dmaps_sv.tactile.gps%26w%3D203%26h%3D100%26yaw%3D87.160706%26pitch%3D0%26thumbfov%3D100!7i13312!8i6656?entry=ttu
    # Set API parameters
    # params_depth = {
    #     'authuser': '0',
    #     'hl': 'en',
    #     'gl': 'us',
    #     'pb': '!1m4!1smaps_sv.tactile!11m2!2m1!1b1!2m2!1sen!2suk!3m3!1m2!1e2!2s' + panoID + '!4m57!1e1!1e2!1e3!1e4!1e5!1e6!1e8!1e12!2m1!1e1!4m1!1i48!5m1!1e1!5m1!1e2!6m1!1e1!6m1!1e2!9m36!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e1!2b0!3e3!1m3!1e4!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e3'
    # }
    params_depth = {
        'authuser': '0',
        'hl': 'ko',
        'gl': 'kr',
        'pb': '!1m4!1smaps_sv.tactile!11m2!2m1!1b1!2m2!1sko!2skr!3m3!1m2!1e2!2s' + panoID + '!4m57!1e1!1e2!1e3!1e4!1e5!1e6!1e8!1e12!2m1!1e1!4m1!1i48!5m1!1e1!5m1!1e2!6m1!1e1!6m1!1e2!9m36!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e1!2b0!3e3!1m3!1e4!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e3'
    }

    # Send GET request to API endpoint and retrieve response
    response = requests.get(endpoint, params=params_depth, proxies=None)
    # response = requests.get(endpoint)

    response = response.content
    response = json.loads(response[4:])
    s = response[1][0][5][0][5][1][2]

    # decode string + decompress zip
    depthMapData = parse(s)
    # parse first bytes to describe data
    header = parseHeader(depthMapData)
    # parse bytes into planes of float values
    data = parsePlanes(header, depthMapData)
    # compute position and values of pixels
    depthMap = computeDepthMap(header, data["indices"], data["planes"])
    # process float 1D array into int 2D array with 255 values
    im = depthMap["depthMap"]

    im[np.where(im == max(im))[0]] = 255
    if min(im) < 0:
        im[np.where(im < 0)[0]] = 0
    im = im.reshape((depthMap["height"], depthMap["width"])).astype(float)
    print(depthMap["height"])
    print(depthMap["width"])

    return im, header