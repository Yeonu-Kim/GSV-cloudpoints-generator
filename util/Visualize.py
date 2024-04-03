import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

def showHist(data):
    plt.hist(data)
    plt.show()

def showImg(img):
    plt.imshow(img)
    plt.show()

def showPts(x, y, z):
    fig = plt.figure(figsize=(15,15))
    ax = plt.axes(projection='3d')
    ax.set_xlabel('$X$', fontsize=20)
    ax.set_ylabel('$Y$', fontsize=20)
    ax.set_zlabel('$Z$', fontsize=20)
    ax.scatter3D(x, y, z, c='b', marker='o')

def showColorMap(map):
    cdict = {
    'red'  :  ( (0.00, 0.99, 0.03), (1.00, 1.99, 0.03), (2.00, 2.99, 0.03)),
    'green':  ( (3.00, 3.99, 0.03), (4.00, 4.99, 0.03), (5.0, 5.99, 0.03)),
    'blue' :  ( (6.00, 6.99, 0.03), (7.00, 7.99, 0.03), (8.0, 8.99, 0.03))
    }
    plt.matshow(map)
    plt.colorbar()
    plt.show