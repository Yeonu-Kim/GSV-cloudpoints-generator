import os
import numpy as np

# Check path
path = r"/home/ywk0524/GSV-cloudpoints-generator"
os.chdir(path)

from module.Generator import createPoints, ignoreSky
from module.DataLoader import loadImg, loadLocalImg
from module.DataSaver import savePts
from monodepth2.test_simple import depthEstimation
from util.Visualize import showHist, showImg, showPts, showColorMap
from skyMask.skyDetection import detectSky
# from skyDetector.sky_detector.detector import get_sky_region_gradient


# Configuration
# 37.2465739,127.0323537
lat = 37.2465739
lon = 127.0323537
APIkey = "YOUR_API_KEY"
savePath = r"/home/ywk0524/GSV-cloudpoints-generator/output"

# Load GSV images and depthmap
image = loadLocalImg(r"/home/ywk0524/GSV-cloudpoints-generator/asset/panorama4.jpg")
# image, panoID = loadImg(lat, lon, APIkey)
showImg(image)
depthMap = depthEstimation(image, 'mono+stereo_1024x320')
showHist(depthMap)
showImg(depthMap)

# Make mask to remove sky
mask = detectSky(image)
showImg(mask)
depthMap = ignoreSky(depthMap, mask)
np.savetxt('./depthmap_output.txt', depthMap)

# mask = get_sky_region_gradient(image)
# showImg(mask)
# depthMap = ignoreSky(depthMap, mask)
# np.savetxt('./depthmap_output.txt', depthMap)

# Create the cloudPoints using depthMap
x, y, z = createPoints(depthMap, lat, lon) # createPoints(depthMap, lat, lon, ignore = False)
showPts(x, y, z)

# Save the coordinate of the cloudpoints
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
z = z.reshape(-1, 1)

result = np.concatenate((x, y, z), axis=1)
np.savetxt('./result_output.txt', result)