import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt


print cv2.__version__

imgName = 'parking-smaller.jpg'
dataFolder = './DATA/parking-sample/'

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(dataFolder+imgName,1)

#-> Image processing
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h,s,v = cv2.split(img_hsv)

v = cv2.equalizeHist(v)

img_hsv = cv2.merge((h, s, v))

img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

img = cv2.GaussianBlur(img, (3,3), 0, 0, cv2.BORDER_DEFAULT)

img = cv2.pyrMeanShiftFiltering(img, 20, 20, 3)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
'''
cv2.medianBlur(gray, 7, gray)

img_edges = cv2.Canny(gray, 33, 66)

element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
closing_img = cv2.morphologyEx(img_edges, cv2.MORPH_CLOSE, element)
result = closing_img
'''

result = cv2.adaptiveThreshold(gray,230, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13, 0)

#Simple Image preview
cv2.imshow('image',gray)
cv2.imshow('processed', result)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
'''
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(dataFolder+'parking-detect.png',final)
    cv2.destroyAllWindows()
'''