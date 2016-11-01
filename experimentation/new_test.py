import cv2
import numpy as np
from random import randint

print cv2.__version__

imgName = 'parking-sample.jpg'
templateName = 'template.jpg'
dataFolder = '../DATA/parking-sample/'

img = cv2.imread(dataFolder+imgName,1)

template = cv2.imread(dataFolder+templateName,0)

img_blur = cv2.bilateralFilter(img,9,75,75)

img_mean = cv2.pyrMeanShiftFiltering(img_blur, 30, 20, 3)

img_gray = cv2.cvtColor(img_mean,cv2.COLOR_BGR2GRAY)

img_median_val = np.median(img_gray)

sigma = 0.33
lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
img_canny = cv2.Canny(img_gray, lower_thresh, upper_thresh)

img_adaptive = cv2.adaptiveThreshold(img_gray, img_median_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13, -1)
img_adaptive = cv2.equalizeHist(img_adaptive)

img_canny_adaptive = np.bitwise_or(img_canny,img_adaptive)


kernel = np.ones((2,2),np.uint8)
img_opening = cv2.morphologyEx(img_canny_adaptive, cv2.MORPH_OPEN, kernel)

template_canny = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("template", template_canny)
contours_template, hierarchy = cv2.findContours(template, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours_template:
    print cv2.contourArea(contour)
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    if len(approx)==4:
        print "Found one"
        cv2.drawContours(img, [contour], 0, (0,0,255),-1)

'''
contour_area_max = 100

for contour in contours_template:
    if cv2.contourArea(contour)>contour_area_max:
        x, y, h, w = cv2.boundingRect(contour)
        roi = img_opening[y:y+h, x:x+w]
        roi_median = np.median(roi)
        print  roi_median
        roi_average = np.average(roi)
        print roi_average
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
'''

#cv2.drawContours(img, contours_template, -1,(0,255,0), 1)
cv2.imshow('Original', img)



k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()