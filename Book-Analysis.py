from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import csv
import os

#Directory and Files
directory_in_str = 'C:\\Users\\emily\\Desktop\\Research\\Baby Books\\Prepped\\'
imgNum = 2
cat = "obj" #bg = background or obj = object
thresh = 70

white = (255, 255, 255)
black = (20, 20, 20)
col1 = (170, 170, 140) 
col2 = (60, 60, 50) 
col3 = (230, 230, 80) 
col4 = (60, 90, 50) 
col5 = (250, 150, 40)
col6 = (125, 180, 40)

cols = [col1, col2]
ncol = len(cols)

def minMax(col):
    colMin = (col[0] - thresh, col[1] - thresh, col[2] - thresh)
    colMax = (col[0] + thresh, col[1] + thresh, col[2] + thresh) 
    return colMin, colMax

mins = []
maxs = []
for col in cols:
    bmin, bmax = minMax(col)
    mins.append(bmin)
    maxs.append(bmax)

    
def compareBackground(color, bMin, bMax):
    if color[0] > bMin[0] and color[1] > bMin[1] and color[2] > bMin[2] and color[0] < bMax[0] and color[1] < bMax[1] and color[2] < bMax[2]:
        return False
    else:
        return True
    
def compareTarget(color, targMin, targMax):
    if color[0] > targMin[0] and color[1] > targMin[1] and color[2] > targMin[2] and color[0] < targMax[0] and color[1] < targMax[1] and color[2] < targMax[2]:
        return True
    else:
        return False
    

def countPix(pic, bgOrObject, nCol):
    #Takes picture as input, converts the picture to RGB values, then counts pixels in objects (as distinct from background)
    #Converts to matrix (1 = object, 0 = background)
    pic_rgb = pic.convert('RGB')
    pix = 0
    width, height = pic.size
    mat = np.zeros((width, height))
    if bgOrObject == "bg":
        for x in range(0, width):
            for y in range(0, height):
                color = pic_rgb.getpixel((x, y))
                ok = 0
                for i in range(0, nCol):
                    if compareBackground(color, mins[i], maxs[i]) == False:
                        ok += 1   
                if ok == 0:
                    pix = pix + 1
                    mat[x,y] = 1
                else:
                    mat[x,y] = 0
                    
    elif bgOrObject == "obj":
        for x in range(0, width):
            for y in range(0, height):
                color = pic_rgb.getpixel((x, y))  
                ok = 0
                for i in range(0, nCol):
                    if compareTarget(color, mins[i], maxs[i]) == False:
                        ok = ok + 1
                if ok < nCol:
                    pix = pix + 1
                    mat[x,y] = 1                     
                else:
                    mat[x,y] = 0
    return(pix, mat)            
    
def convexHull(matx):
    #Calculates convex hull around objects
    obj = np.argwhere(matx == 1).tolist()
    objPoints = np.asarray(obj)
    ch = ConvexHull(objPoints)
    chArea = ch.area
    
    #plt.plot(objPoints[:,0], objPoints[:,1], 'o', color = 'blue')
    #for simplex in ch.simplices:
        #plt.plot(objPoints[simplex, 0], objPoints[simplex, 1], color ='blue')     
    #plt.show()   
    return (chArea)

def totalPerim(mat):
    width, height = mat.shape
    perim = 0
    perimMat = np.zeros((width, height))
    for x in range(0, width):
        for y in range(0, height):
            val = mat[x, y]
            #If yellow, find number of yellow neighbors, and if not all 4 neighbors are yellow, count this as a perimeter pixel
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
            
    perimPoints= np.argwhere(perimMat == 1).tolist()
    perimPoints = np.asarray(perimPoints)  
    plt.plot(perimPoints[:,0], perimPoints[:,1], 'o', color = 'black')
    plt.show()
    return perim

def blackAndWhite(mat,saveName):
    width, height = mat.shape
    img = Image.new('RGB', (width,height), color = (255, 255, 255))
    pixels = img.load()
    for x in range(0, width):
        for y in range(0, height):
            if mat[x,y] == 1:
                pixels[x,y] = (0,0,0)
            else:
                pixels[x,y] = (255,255,255)  
    img.show()
    img.save(saveName)

def imageAnalysis(pic, bgOrObject, nCol, saveName):
    tsa, mat = countPix(pic, bgOrObject, nCol)
    #ch = convexHull(mat)
    #perim = totalPerim(mat)
    blackAndWhite(mat, saveName)
    #columnTitleRow = ["TSA", "CH", "Perim"]
    #with open(fileName, 'wb') as outfile:
        #writer = csv.writer(outfile)
        #writer.writerow(columnTitleRow)
        #writer.writerow([tsa, ch, perim])   


#fileName = "analysis_" + str(imgNum) + ".csv"
image = str(imgNum) + ".png"
os.chdir(directory_in_str)
img = Image.open(image)  
imageAnalysis(img, cat, ncol)