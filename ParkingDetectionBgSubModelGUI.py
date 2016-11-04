import cv2
import os

from ParkingDetection import ParkingDetection


class BgSubModelParkingDetection(ParkingDetection):
    def detectParking(self, imgPath, emptyFolderPath):

        # Load image and edit path of empty folder
        emptyFolder = emptyFolderPath + '/'
        img = cv2.imread(imgPath, 1)

        # Image to gray and list images inside empty folder provided
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        images = [f for f in os.listdir(emptyFolder) if os.path.isfile(os.path.join(emptyFolder, f))]

        # New BackgroundSubtractorMOG2 object
        bgs_mog = cv2.BackgroundSubtractorMOG2()

        # Model the background based on blurred gray images - reduce noise
        for image in images:
            bgImageFile = cv2.imread(emptyFolder + image, 0)
            bgImageFile_blur = cv2.GaussianBlur(bgImageFile, (21, 21), 0)
            bgs_mog.apply(bgImageFile_blur, learningRate=1)

        # Blur image
        img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0)

        # Get foreground mask by applying BackgroundSubtractorMOG2 on blurred image
        fg_mask = bgs_mog.apply(img_blur, learningRate=0)

        # Threshold the foreground mask
        mask = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY_INV)[1]

        # Dilate mask to increase chance of closing a contour
        mask = cv2.dilate(mask, None, iterations=2)

        # Extract all contours in mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours by area limitation and draw rectangles around them(cars)
        contour_area_min = 250
        contour_area_max = 2500
        for contour in contours:
            if ((cv2.contourArea(contour) < contour_area_max) and (cv2.contourArea(contour) > contour_area_min)):
                (x, y, h, w) = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Result", img)
        cv2.waitKey()
        cv2.destroyAllWindows()

        return
