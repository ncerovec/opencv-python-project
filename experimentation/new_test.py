import cv2
import numpy as np
from random import randint

print cv2.__version__

imgName = 'parking-sample.jpg'
templateName = 'template.jpg'
dataFolder = '../DATA/parking-sample/'

img = cv2.imread(dataFolder+imgName,1)

template = cv2.imread(dataFolder+templateName,1)

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

template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template_canny = cv2.Canny(template, 50, 100)

contours_template, hierarchy = cv2.findContours(template_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_area_min = 100
for contour in contours_template:
    if cv2.contourArea(contour)>contour_area_min:
        x, y, w, h = cv2.boundingRect(contour)
        roi = img_opening[y:y+h, x:x+w]
        roi_average = np.average(roi)
        if (roi_average > 30):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

cv2.imshow('Original', img)


k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()