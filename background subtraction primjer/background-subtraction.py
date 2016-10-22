import cv2
import numpy as np

PARKING_SPACES = 40

def detectSqrContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def grayScale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def drawContours(img, contours):
    global PARKING_SPACES
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 25:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
            PARKING_SPACES -= 1
    return img

backgroundImage = cv2.imread('empty.jpg',1)
currentImage = cv2.imread('parkinglot.jpg',1)
diffImage = cv2.absdiff(backgroundImage, currentImage)

'''
imageWidth = diffImage.shape[1] #Get image width  cols
imageHeight = diffImage.shape[0] #Get image height rows


foregroundMask = np.zeros((imageHeight, imageWidth))

threshold = 30.0

i = 0
j = 0
while i<imageHeight:
    while j<imageWidth:
        pix = diffImage[100, 100]
        dist = (pix[0] * pix[0] + pix[1] * pix[1] + pix[2] * pix[2])
        dist = dist * dist
        if dist > threshold:
            foregroundMask[i,j] = 255
        j+=1
    i+=1
'''
contours = detectSqrContours(grayScale(diffImage))



result = drawContours(currentImage, contours)

print 'Slobodnih mjesta: '+str(PARKING_SPACES)

cv2.imshow('result',result)
#cv2.imshow('result2',foregroundMask)
k = cv2.waitKey(0)