import cv2
import os
import numpy as np

print cv2.__version__

dataFolder = '../DATA/pklot/'

number_of_images = len([name for name in os.listdir(dataFolder) if os.path.isfile(os.path.join(dataFolder, name))])
images = [f for f in os.listdir(dataFolder+"empty/") if os.path.isfile(os.path.join(dataFolder+"empty/", f))]

print "Images found:" + str(number_of_images)

bgs_mog = cv2.BackgroundSubtractorMOG2(history=500, varThreshold=500, bShadowDetection=True)

for image in images:
    print "Opening image:"+image
    bgImageFile = cv2.imread(dataFolder+"empty/"+ image)

    bgs_mog.apply(bgImageFile, learningRate=0.5)

test_image = cv2.imread(dataFolder+"pklot275.jpg")
fg_mask = bgs_mog.apply(test_image, learningRate=0)

cv2.imshow("Original", test_image)
cv2.imshow("Mask", fg_mask)

cv2.waitKey()
cv2.destroyAllWindows()