import cv2
import numpy as np
from random import randint
from matplotlib import pyplot as plt

print cv2.__version__

imgName = 'parking-sample.jpg'
template_name = 'template.jpg'
dataFolder = '../DATA/parking-sample/'

img = cv2.imread(dataFolder+imgName,1)
'''
template = cv2.imread(dataFolder+template_name,1)

img_blur = cv2.bilateralFilter(img,9,75,75)
template_blur = cv2.bilateralFilter(template,9,75,75)

img_mean = cv2.pyrMeanShiftFiltering(img_blur, 30, 20, 3)
template_mean = cv2.pyrMeanShiftFiltering(template_blur, 30, 20, 3)

img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)

img_median_val = np.median(img_gray)
template_median_val = np.median(template_gray)
print img_median_val, template_median_val

sigma = 0.33
lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
img_canny = cv2.Canny(img_gray, lower_thresh, upper_thresh)

sigma = 0.33
lower_thresh_templ = int(max(0, (1.0 - sigma) * template_median_val))
upper_thresh_templ = int(min(255, (1.0 + sigma) * template_median_val))
template_canny = cv2.Canny(template_gray, lower_thresh_templ, upper_thresh_templ)


img_adaptive = cv2.adaptiveThreshold(img_gray, img_median_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13, -1)
img_adaptive = cv2.equalizeHist(img_adaptive)

img_canny_adaptive = np.bitwise_or(img_canny,img_adaptive)


kernel = np.ones((2,2),np.uint8)
img_opening = cv2.morphologyEx(img_canny_adaptive, cv2.MORPH_OPEN, kernel)


template_adaptive = cv2.adaptiveThreshold(template_gray, template_median_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13, -1)
img_adaptive = cv2.equalizeHist(template_adaptive)

template_canny_adaptive = np.bitwise_or(template_canny,template_adaptive)

template_opening = cv2.morphologyEx(template_canny_adaptive, cv2.MORPH_OPEN, kernel)



h, w = template.shape[:2]


res = cv2.matchTemplate(img_opening,template_opening,cv2.TM_SQDIFF_NORMED)
threshold = 0.75
loc = np.where( res <= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
'''

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

dst = cv2.cornerHarris(img_gray,5,3,0.1)

dst = cv2.dilate(dst,None)

img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()