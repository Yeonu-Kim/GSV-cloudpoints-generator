import numpy as np

# Convert wgs to utm
def getCartesian(lat, lon):
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371000 # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    return x,y,z

def ignoreSphere(depthMap):
    return depthMap*(depthMap<255)

# Create cloud points using depthmap
# magic number = 100(maximum range of LIDAR)
def createPoints(header, depthMap, lat, lon, ignore=True):
    if (ignore==True):
        depthMap = ignoreSphere(depthMap)
    
    '''
    int x,y,xs,ys      # texture positiona and size
    double a,b,r,da,db # spherical positiona and angle steps
    double xx,yy,zz    # 3D point
    '''
    xs=header['width']
    ys=header['height']
   
    # 360x90 deg
    da=4.0*np.pi/(xs-1)
    db=0.5*np.pi/(ys-1)
    a=0.0
    b=0.0
    
    '''
    # 180x90 deg
    da=1.0*M_PI/(xs-1)
    db=0.5*M_PI/(ys-1)
    a=0.0
    b=-0.25*M_PI
    '''

    # Calculate the angle a(x angle), b(y angle) in spherical coor
    A=np.full(ys, a)
    for idx, angle in enumerate(A):
        angle+=idx*da
        A[idx]=angle
    A=np.repeat(A, repeats=xs, axis=0)
    A=A.reshape(xs, ys)
    A=A.T
    # plt.imshow(A)
    # plt.title("A image")
    # plt.show()
    
    B = np.full(xs, b)
    for idx, angle in enumerate(B):
        angle+=idx*db
        B[idx]=angle
    B=np.repeat(B, repeats=ys, axis=0)
    B=B.reshape(ys, xs)
    # plt.imshow(B)
    # plt.title("B image")
    # plt.show()

    # Calculate the cartesian coor of cloud points
    xx = 100*depthMap*np.sin(B)*np.cos(A)
    yy = 100*depthMap*np.sin(B)*np.sin(A)
    zz = 100*depthMap*np.cos(B)

    xx_new, yy_new, _ = getCartesian(lat, lon)
    xx+=xx_new
    yy+=yy_new

    return xx, yy, zz