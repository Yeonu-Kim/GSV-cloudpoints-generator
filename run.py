from module.DataLoader import panoDataLoader, depthDataLoader
from module.Preprocessor import stitchPano
from module.Generator import decodeBase64, makeDepthMap, makeCloudPoints
from util.Visualization import showPano, showDepth, showCloudPoints

panoID = "ChIJeRpOeF67j4AR9ydy_PIzPuM" # Configuration 
APIkey = ""

panoTiles = panoDataLoader(panoID, APIkey)
panoImg = stitchPano(panoTiles)
showPano(panoImg)

base64Depth = depthDataLoader(panoID)
depthData = decodeBase64(base64Depth)
depthMap = makeDepthMap(depthData)
showDepth(depthMap)

cloudPoints = makeCloudPoints(depthData)
showCloudPoints(cloudPoints)