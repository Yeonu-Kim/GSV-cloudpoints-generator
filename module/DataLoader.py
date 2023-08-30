import requests
import numpy as np

def panoDataLoader(panoID, APIkey):
    # Set panoTiles (result) empty list
    panoTiles = np.array([])
    
    # Set payload and headers empty
    payload = {}
    headers = {}

    # Download 3 pano tiles using GSV API (0, 120, 240 degree)
    for i in range(3):
        url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&pano={panoID}&fov=120&heading={i*120}&key={APIkey}"
        reponse = requests.request("GET", url, headers = headers, data = payload)
    
        # Extract the image byte data
        panoTile = reponse.content
        panoTiles = panoTiles.append(panoTile)
    
    return panoTiles

def depthDataLoader(panoID):
    return 0