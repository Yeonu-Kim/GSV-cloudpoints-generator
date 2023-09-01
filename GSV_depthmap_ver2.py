import base64
import zlib
import numpy as np
import struct
import matplotlib.pyplot as plt
import requests
import json
import io
from PIL import Image
import math

def parse(b64_string):
    # fix the 'inccorrect padding' error. The length of the string needs to be divisible by 4.
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    # convert the URL safe format to regular format.
    data = b64_string.replace("-", "+").replace("_", "/")

    data = base64.b64decode(data)  # decode the string
    # data = zlib.decompress(data)  # decompress the data
    return np.array([d for d in data])


def parseHeader(depthMap):
    return {
        "headerSize": depthMap[0],
        "numberOfPlanes": getUInt16(depthMap, 1),
        "width": getUInt16(depthMap, 3),
        "height": getUInt16(depthMap, 5),
        "offset": getUInt16(depthMap, 7),
    }


def get_bin(a):
    ba = bin(a)[2:]
    return "0" * (8 - len(ba)) + ba


def getUInt16(arr, ind):
    a = arr[ind]
    b = arr[ind + 1]
    return int(get_bin(b) + get_bin(a), 2)


def getFloat32(arr, ind):
    return bin_to_float("".join(get_bin(i) for i in arr[ind : ind + 4][::-1]))


def bin_to_float(binary):
    return struct.unpack("!f", struct.pack("!I", int(binary, 2)))[0]


def parsePlanes(header, depthMap):
    indices = []
    planes = []
    n = [0, 0, 0]

    for i in range(header["width"] * header["height"]):
        indices.append(depthMap[header["offset"] + i])

    for i in range(header["numberOfPlanes"]):
        byteOffset = header["offset"] + header["width"] * header["height"] + i * 4 * 4
        n = [0, 0, 0]
        n[0] = getFloat32(depthMap, byteOffset)
        n[1] = getFloat32(depthMap, byteOffset + 4)
        n[2] = getFloat32(depthMap, byteOffset + 8)
        d = getFloat32(depthMap, byteOffset + 12)
        planes.append({"n": n, "d": d})

    return {"planes": planes, "indices": indices}


def computeDepthMap(header, indices, planes):

    v = [0, 0, 0]
    w = header["width"]
    h = header["height"]

    depthMap = np.empty(w * h)

    sin_theta = np.empty(h)
    cos_theta = np.empty(h)
    sin_phi = np.empty(w)
    cos_phi = np.empty(w)

    for y in range(h):
        theta = (h - y - 0.5) / h * np.pi
        sin_theta[y] = np.sin(theta)
        cos_theta[y] = np.cos(theta)

    for x in range(w):
        phi = (w - x - 0.5) / w * 2 * np.pi + np.pi / 2
        sin_phi[x] = np.sin(phi)
        cos_phi[x] = np.cos(phi)

    for y in range(h):
        for x in range(w):
            planeIdx = indices[y * w + x]

            v[0] = sin_theta[y] * cos_phi[x]
            v[1] = sin_theta[y] * sin_phi[x]
            v[2] = cos_theta[y]

            if planeIdx > 0:
                plane = planes[planeIdx]
                t = np.abs(
                    plane["d"]
                    / (
                        v[0] * plane["n"][0]
                        + v[1] * plane["n"][1]
                        + v[2] * plane["n"][2]
                    )
                )
                depthMap[y * w + (w - x - 1)] = t
            else:
                depthMap[y * w + (w - x - 1)] = 9999999999999999999.0
    return {"width": w, "height": h, "depthMap": depthMap}

def ignoreSphere(depthMap):
    return depthMap*(depthMap<255)

def createPoints(header, depthMap):
    '''
    int x,y,xs,ys      # texture positiona and size
    double a,b,r,da,db # spherical positiona and angle steps
    double xx,yy,zz    # 3D point
    '''
    M_PI = 3.14159265358979323846
    xs=header['width']
    ys=header['height']

    
    '''
    # 360x180 deg
    da=2.0*M_PI/(xs-1)
    db=1.0*M_PI/(ys-1)
    a=0.0
    b=-0.5*M_PI
    '''
    
    # 180x90 deg
    da=1.0*M_PI/(xs-1)
    db=0.5*M_PI/(ys-1)
    a=0.0
    b=-0.25*M_PI
    
    
    # normalize to <0..1>
    depthMap/=255

    # Calculate the angle a(x angle), b(y angle) in spherical coor
    a = np.full((xs), a, dtype=float)
    for idx, angle in enumerate(a):
        angle+=idx*da
        a[idx]=angle
    a=np.repeat(a, repeats=ys, axis=0)
    a=a.reshape(ys, xs)

    b=np.full((ys), b, dtype=float)
    for idx, angle in enumerate(b):
        angle+=idx*db
        b[idx]=angle
    b=np.repeat(b, repeats=xs, axis=0)
    b=b.reshape(xs, ys)
    b=b.T

    # Calculate the cartesian coor of cloud points
    xx = depthMap*np.cos(a)*np.cos(b)
    yy = depthMap*np.sin(a)*np.cos(b)
    zz = depthMap*          np.sin(b)

    return xx, yy, zz

def visualize_3D_pts(x, y, z):
    fig = plt.figure(figsize=(15,15))
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, z, c='b', marker='o')

endpoint = 'https://maps.googleapis.com/maps/api/streetview/metadata'

params = {
    'location': '39.7679158,-86.1580276',
    'key': 'YOUR_API_KEY',
}

url = f"https://maps.googleapis.com/maps/api/streetview?size=400x300&location={params['location']}&key={params['key']}"

payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

# 이미지 바이트 데이터
bytes_data = response.content

image = Image.open(io.BytesIO(bytes_data))
plt.imshow(image)
plt.show()

r = requests.get(endpoint, params=params)
pano_id = r.json()['pano_id']

# Set API endpoint URL
endpoint = 'https://www.google.com/maps/photometa/v1'

# Set API parameters
params_depth = {
    'authuser': '0',
    'hl': 'en',
    'gl': 'us',
    'pb': '!1m4!1smaps_sv.tactile!11m2!2m1!1b1!2m2!1sen!2suk!3m3!1m2!1e2!2s' + pano_id + '!4m57!1e1!1e2!1e3!1e4!1e5!1e6!1e8!1e12!2m1!1e1!4m1!1i48!5m1!1e1!5m1!1e2!6m1!1e1!6m1!1e2!9m36!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e1!2b0!3e3!1m3!1e4!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e3'
}

# Send GET request to API endpoint and retrieve response
response = requests.get(endpoint, params=params_depth, proxies=None)
# response = requests.get(endpoint)

# Extract image and depth map from response
print(response.links)
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
# display image
plt.imshow(im)
plt.show()

im=ignoreSphere(im)
print(im)
x, y, z = createPoints(header, im)
visualize_3D_pts(z, y, x)
