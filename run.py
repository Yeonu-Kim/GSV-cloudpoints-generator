import os

# Check path
path = r"C:\Users\82103\Desktop\GSV-cloudpoints-generator"
os.chdir(path)

from module.Generator import createPoints
from util.Visualize import showHist, showImg, showPts
from module.DataLoader import loadImg, loadDepth
from module.DataSaver import savePts, integratePts

# Configuration
# 37.281575,127.0017723
lat = 37.281575
lon = 127.0017723
APIkey = "YOUR_API_KEY"
savePath = r"C:\Users\82103\Desktop\GSV-cloudpoints-generator\output"

# Load GSV images and depthmap
image, panoID = loadImg(lat, lon, APIkey)
showImg(image)
depthMap, header = loadDepth(
    panoID
)  # header is the dictionary that show the width and the height of depthmap
showHist(depthMap)
showImg(depthMap)

# Create the cloudPoints using depthMap
# createPoints(header, depthMap, lat, lon, ignoreSphere(optional)=True)
x, y, z = createPoints(header, depthMap, lat, lon)
showPts(x, y, z)

# Save the coordinate of the cloudpoints
savePts(x, y, z, savePath)
