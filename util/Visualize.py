import matplotlib.pyplot as plt

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
