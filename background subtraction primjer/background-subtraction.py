import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

from ParkingDetectionSubstraction import SubstractionParkingDetection

#TODO:
    #Order image processing and filtering for best results
    #Implement parking spot size detection (average of most of contures with size ratio 2:3)
    #Detect cars and parking spots - print the number of empty and full parking spots


def canny(img):
    sigma = 0.33
    img_median_val = np.median(img)
    lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
    upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
    canny = cv2.Canny(img, lower_thresh, upper_thresh)
    return canny


def detectSqrContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def drawContours(img, contours):
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        print w,h
        if(x < 500 and h <500):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
    return img

fileTypes = [('JPG', '.jpg'), ('PNG', '.png')]
dataFolder = '../DATA/'

sampleFolder = './parking-sample/'
imgOpen = './parking-full-top-small.jpg'
imgSave = './parking-detect.png'

filePath = dataFolder+sampleFolder+imgOpen

pklotFolder = 'parking-pkLot/'
imgSubOpen = 'parking-2.jpg'
imgSubOpenBG = 'parking-1.jpg'

filePathSub = dataFolder+pklotFolder+imgSubOpen
filePathSubBG = dataFolder+pklotFolder+imgSubOpenBG

#Open file select dialog
#fo = FileOperations(fileTypes, str(dataFolder+sampleFolder), dataFolder, imgOpen, imgSave)
#filePath = fo.openFileDialog()

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(filePath,1)
imgSub = cv2.imread(filePathSub,1)
imgBG = cv2.imread(filePathSubBG,1)

diffImage = cv2.absdiff(imgSub, imgBG);

#Parking detection using background substraction
img = diffImage


ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
titles = ['Original Image', 'BINARY', 'TOZERO']

images = [img, thresh1, thresh4]

#cv2.imshow('detection',img)
#cv2.imshow('detection',thresh1)

workImg = thresh2

gray = cv2.cvtColor(workImg, cv2.COLOR_BGR2GRAY)

#sobelx8u = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=5)
#canny = canny(sobelx8u)

contours = detectSqrContours(gray)

result = drawContours(imgSub, contours)

cv2.imshow('detection',result)

#-> Image save & end program

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    #fo.saveFileDialog(img)
    cv2.imwrite(dataFolder+imgSave,img)
    cv2.destroyAllWindows()
