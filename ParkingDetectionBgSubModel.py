import cv2
import os
import numpy as np

from ParkingDetection import ParkingDetection

class BgSubModelParkingDetection(ParkingDetection):

    def detectParking(self, img, emptyFolder):
        images = [f for f in os.listdir(emptyFolder) if os.path.isfile(os.path.join(emptyFolder, f))]

        bgs_mog = cv2.BackgroundSubtractorMOG2()

        for image in images:
            bgImageFile = cv2.imread(emptyFolder+image,0)
            bgImageFile_blur = cv2.GaussianBlur(bgImageFile, (21,21),0)
            bgs_mog.apply(bgImageFile_blur, learningRate=1)

            print "Model extracted..."

            test_image_blur = cv2.GaussianBlur(img, (21,21),0)

            fg_mask = bgs_mog.apply(test_image_blur, learningRate=0)

            mask = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY_INV)[1]

            mask = cv2.dilate(mask,None, iterations=2)

            return mask
