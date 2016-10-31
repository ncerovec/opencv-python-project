import cv2
import os
import numpy as np

print cv2.__version__

dataFolder = '../DATA/PKlot/'
emptyFolder = '../DATA/PKlot/empty/'

images = [f for f in os.listdir(emptyFolder) if os.path.isfile(os.path.join(emptyFolder, f))]

bgs_mog = cv2.BackgroundSubtractorMOG2()

for image in images:
    #print "Opening image:"+image
    bgImageFile = cv2.imread(emptyFolder+ image,0)
    bgImageFile_blur = cv2.GaussianBlur(bgImageFile, (21,21),0)
    bgs_mog.apply(bgImageFile_blur, learningRate=1)

print "Model done"

test_image = cv2.imread(dataFolder+"pklot295.jpg",0)
test_image_blur = cv2.GaussianBlur(test_image, (21,21),0)

fg_mask = bgs_mog.apply(test_image_blur, learningRate=0)

mask = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY_INV)[1]

mask = cv2.dilate(mask,None, iterations=2)
contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

contour_area_min = 250
contour_area_max = 2500
for contour in contours:
    if ((cv2.contourArea(contour) < contour_area_max)and(cv2.contourArea(contour) > contour_area_min)):
        (x, y, h, w) = cv2.boundingRect(contour)
        cv2.rectangle(test_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Original", test_image)
cv2.imshow("Mask", mask)


cv2.waitKey()
cv2.destroyAllWindows()