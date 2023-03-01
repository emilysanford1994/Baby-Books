from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
from pathlib2 import Path
import matplotlib.pyplot as plt
import csv
import os

# Before running, you will need to specify the directory where the images are stored (in line 12) and how many folders deep the image are saved (line 139).

# Directory where images are saved
directory_in_str = ' '
os.chdir(directory_in_str)

# File where feature information is to be saved
fileName = "Feature Information.csv"

# This code works with two-color images (different color for background and foreground).
# Specify the color of the objects whose features are to be extracted. In our dataset, the objects are black and the background is white. 
black = (0,0,0)



#######################################################
#Functions

def countPix(pic):
    #Takes picture as input, converts the picture to RGB values, then counts pixels in objects (as distinct from background)
    #Converts to matrix (1 = object, 0 = background)
    
    pic_rgb = pic.convert('RGB')
    pix = 0
    width, height = pic.size
    mat = np.zeros((width, height))
    for x in range(0, width):
        for y in range(0, height):
            color = pic_rgb.getpixel((x, y))
            if color[0] == black[0]:
                pix = pix + 1
                mat[x,y] = 1
            else:
                mat[x,y] = 0
    return(pix, mat, height, width)            
    
    
    
def convexHull(matx):
    # Calculates convex hull around objects
    # Note that chArea = area within the convex hull; chPerimeter = the perimeter of the convex hull.
    
    obj = np.argwhere(matx == 1).tolist()
    objPoints = np.asarray(obj)
    ch = ConvexHull(objPoints)
    chArea = ch.volume
    chPerim = ch.area
    
    # To visualize the convex hull around the objects, uncomment the following:
    
    #plt.plot(objPoints[:,0], objPoints[:,1], 'o', ms = .5, color = 'gray')
    #for simplex in ch.simplices:
        #plt.plot(objPoints[simplex, 0], objPoints[simplex, 1], "--", ms = 5, color ='black')     
    #plt.show()   
    
    return (chArea, chPerim)



def totalPerim(mat):
    # Calculates the total perimeter around all objects
    width, height = mat.shape
    perim = 0
    perimMat = np.zeros((width, height))
    for x in range(0, width):
        for y in range(0, height):
            val = mat[x, y]
            #If obj, find number obj neighbors, and if not all 4 neighbors are obj, count this as a perimeter pixel
            if val == 1:
                left = mat[x - 1, y]
                right = mat[x+1, y]
                up = mat[x, y-1]
                down = mat[x, y+1]
                neighbors = 0
                for neighbor in [left, right, up, down]:
                    if neighbor == 1:
                        neighbors = neighbors + 1
                if neighbors < 4:
                    perim = perim + 1
                    perimMat[x,y] = 1
            
    # To visualize the total perimeter of the objects, uncomment the following:
    
    #perimPoints= np.argwhere(perimMat == 1).tolist()
    #perimPoints = np.asarray(perimPoints)  
    #plt.plot(perimPoints[:,0], perimPoints[:,1], 'bo', ms = .8)
    #plt.show()
    return perim



def getCenter(mat):
    # Finds the center of the image
    
    pointList = np.argwhere(mat == 1).tolist()
    x = [p[0] for p in pointList]
    y = [p[1] for p in pointList]
    centerX = (max(x)+min(x)) / 2
    centerY = (max(y)+min(y))/2
    return centerX, centerY



def imageAnalysis(pic, book, n):
    # Performs the image analysis over a given image, extracting the height, width, center coordinates, surface area, convex hull, and perimeter
    
    tsa, mat, height, width = countPix(pic)
    chA, chP = convexHull(mat)
    perim = totalPerim(mat)
    centerX, centerY = getCenter(mat)
    return tsa, height, width, chA, chP, perim, centerX, centerY

#######################################################


# Running the image analysis

# Create list of images to be analyzed
images = []
pathlist = Path(directory_in_str).glob('**/*.png')
for path in pathlist:
    path_in_str = str(path)
    images.append(path_in_str)


# Run through image analysis 
i = 1  
rows = []
columnTitleRow = ["Name", "Book", "Version","N", "TSA", "CH_area", "CH_perimeter", "Perim", "height", "width", "centerX", "centerY"]
for image in images: 
    picName = image.split("/",9)[9] # change this to the correct number for your file storage system
    book = picName.split("_",1)[0]
    n = picName.split("_",2)[1]
    version = picName.split("_",2)[2].split(".",1)[0]
    print(i, picName, version) # Keep track of how many images have been analyzed
    img = Image.open(image)  
    tsa, height, width, chA, chP, perim, centerX, centerY = imageAnalysis(img, book, n)
    row = [picName] + [book] +[version]+ [n] + [tsa] + [chA] + [chP] + [perim] + [height] + [width] + [centerX] + [centerY]
    rows.append(row)    
    i = i + 1
       
# Write data to csv
with open(fileName, 'wb') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(columnTitleRow)
    for i in range(0, len(rows)):
        writer.writerow(rows[i]) 
        
        