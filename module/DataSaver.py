import numpy as np
import sys, os
import glob

sys.path.append(os.pardir)

def savePts(x, y, z, savePath):
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    z = z.reshape(-1, 1)

    result = np.concatenate((x, y, z), axis=1)
    savePath = savePath +r'/result_point.txt'
    np.savetxt(savePath, result)

def integratePts(savePath):
    fileList = glob.glob(os.path.join('../output', '*txt'))
    with open('../output/merge.txt', 'w') as outfile:
        for filename in sorted(fileList):
            with open(filename) as file:        
                outfile.write(file.read())