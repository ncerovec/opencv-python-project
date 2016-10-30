import cv2
import numpy as np
import os
from random import randint
from matplotlib import pyplot as plt

print cv2.__version__

imgName = 'parking-sample.jpg'
dataFolder = '../DATA/parking-sample/'
templateFolder = '../DATA/parking-sample/templates/'

img = cv2.imread(dataFolder+imgName,1)
img_blur = cv2.bilateralFilter(img,9,75,75)
img_mean = cv2.pyrMeanShiftFiltering(img_blur, 30, 20, 3)
img_gray = cv2.cvtColor(img_mean,cv2.COLOR_BGR2GRAY)
img_median_val = np.median(img_gray)

sigma = 0.33
lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
img_canny = cv2.Canny(img_gray, lower_thresh, upper_thresh)


template_names  = [f for f in os.listdir(templateFolder) if os.path.isfile(os.path.join(templateFolder, f))]

print template_names

threshold = 0.4

for template_name in template_names:
    template = cv2.imread(templateFolder+template_name)
    template_blur = cv2.bilateralFilter(template,9,75,75)
    template_mean = cv2.pyrMeanShiftFiltering(template_blur, 30, 20, 3)
    template_gray = cv2.cvtColor(template_mean,cv2.COLOR_BGR2GRAY)
    template_median_val = np.median(template_gray)
    lower_thresh_templ = int(max(0, (1.0 - sigma) * template_median_val))
    upper_thresh_templ = int(min(255, (1.0 + sigma) * template_median_val))
    template_canny = cv2.Canny(template_gray, lower_thresh_templ, upper_thresh_templ)
    h, w = template.shape[:2]
    res = cv2.matchTemplate(img_canny,template_canny,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imshow("Result", img)

cv2.waitKey()