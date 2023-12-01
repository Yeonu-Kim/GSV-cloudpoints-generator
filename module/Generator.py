import cv2
import numpy as np
import matplotlib.pyplot as plt

# Convert wgs to utm
def getCartesian(lat, lon):
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371000 # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    return x,y,z

def ignoreSphere(depthMap):
    # depthMap = depthMap[100:220][:]
    return depthMap*(depthMap<5)

def ignoreSky(depthMap, mask):
    _, mask_binary = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    result = depthMap * (mask_binary[:, :, 0] == 0)

    return result

def createPoints(depthMap, lat, lon, ignore = False):
    # preprocess the depth map
    if ignore:
        depthMap = ignoreSphere(depthMap)
    plt.imshow(depthMap)
    plt.show()

    ys, xs = depthMap.shape
   
    phi = 2.0 * np.pi
    theta = 0.5 * np.pi

    # 360x180 deg
    da = phi / xs
    db = theta / ys
    a = np.arange(0, phi, da)
    b = np.arange(theta/2, -theta/2, -db)

    A, B = np.meshgrid(a, b)
    np.flip(B, axis=0)

    # Calculate the cartesian coordinates of cloud points
    xx = depthMap * np.cos(B) * np.cos(A)
    yy = depthMap * np.cos(B) * np.sin(A)
    zz = depthMap * np.sin(B)

    xx_new, yy_new, _ = getCartesian(lat, lon)
    xx += xx_new
    yy += yy_new

    return xx, yy, zz

# def preprocessDepthMap(depthMap, ignore=False):

#     h, w = depthMap.shape
#     v = [0, 0, 0]

#     sin_theta = np.empty(h)
#     cos_theta = np.empty(h)
#     sin_phi = np.empty(w)
#     cos_phi = np.empty(w)

#     for y in range(h):
#         theta = (h - y - 0.5) / h * np.pi
#         sin_theta[y] = np.sin(theta)
#         cos_theta[y] = np.cos(theta)

#     for x in range(w):
#         phi = (w - x - 0.5) / w * 2 * np.pi + np.pi/2
#         sin_phi[x] = np.sin(phi)
#         cos_phi[x] = np.cos(phi)
    
#     for y in range(h):
#         for x in range(w):
#             v[0] = sin_theta[y] * cos_phi[x]
#             v[1] = sin_theta[y] * sin_phi[x]
#             v[2] = cos_theta[y]

#             depth = depthMap[y][x]
#             t = np.abs(depth/(v[0] * depth + v[1] * depth+ v[2] *depth))

#             depthMap[y][x] = t
    
#     return depthMap