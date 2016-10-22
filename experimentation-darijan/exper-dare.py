import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt


print cv2.__version__

imgName = 'parking-full-top.jpg'
print imgName
#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
foregroundMask = np.zeros((60, 60))
img = cv2.imread(imgName,1)


#-> Image processing
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h,s,v = cv2.split(img_hsv)

v = cv2.equalizeHist(v)

img_hsv = cv2.merge((h, s, v))

img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

img = cv2.GaussianBlur(img, (3,3), 0, 0, cv2.BORDER_DEFAULT)

img = cv2.pyrMeanShiftFiltering(img, 20, 20, 3)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.medianBlur(gray, 7, gray)




result = cv2.adaptiveThreshold(gray,230, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13, 0)

img_edges = cv2.Canny(gray, 33, 66)

element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
closing_img = cv2.morphologyEx(img_edges, cv2.MORPH_CLOSE, element)
result = closing_img

contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if (w > 50 and h > 25):# and (w < 300 and h < 100):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)

#Simple Image preview
cv2.imshow('image',result)
cv2.imshow('processed', img)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
'''
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(dataFolder+'parking-detect.png',final)
    cv2.destroyAllWindows()
'''