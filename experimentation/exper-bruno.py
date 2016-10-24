import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt


print cv2.__version__

imgName = 'parking-smaller.jpg'
dataFolder = '../DATA/parking-sample/'

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(dataFolder+imgName,1)

#-> Image processing
img = cv2.GaussianBlur(img, (3,3), 0, 0, cv2.BORDER_DEFAULT)

img = cv2.pyrMeanShiftFiltering(img, 20, 20, 3)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_black = np.array([0,0,0])
upper_black = np.array([180,255,50])

lower_white = np.array([0,0,200])
upper_white = np.array([180,255,255])

lower_red0 = np.array([0,100,100])
upper_red0 = np.array([10,255,255])

lower_red1 = np.array([160,100,100])
upper_red1 = np.array([179,255,255])

lower_blue = np.array([100,150,0])
upper_blue = np.array([140,255,255])

lower_green = np.array([75,100,100])
upper_green = np.array([75,255,255])

lower_yellow = np.array([20,100,100])
upper_yellow = np.array([30,255,255])

lower_orange = np.array([14,0,0])
upper_orange = np.array([16,255,255])

mask_red0 = cv2.inRange(img_hsv, lower_red0, upper_red0)
mask_red1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

mask_red = cv2.addWeighted(mask_red0, 1, mask_red1, 1, 1)

mask_black = cv2.inRange(img_hsv, lower_black, upper_black)
mask_white = cv2.inRange(img_hsv, lower_white, upper_white)

mask_black_white = cv2.addWeighted(mask_black, 1, mask_white, 1, 0)
mask = cv2.addWeighted(mask_red, 1, mask_black_white, 1, 1)

cv2.imshow('mask', mask)

'''
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.medianBlur(gray, 7, gray)

img_edges = cv2.Canny(gray, 33, 66)

result = cv2.adaptiveThreshold(gray,230, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13, 0)

#Simple Image preview
cv2.imshow('image',gray)
cv2.imshow('processed', result)
'''
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
'''
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(dataFolder+'parking-detect.png',final)
    cv2.destroyAllWindows()
'''