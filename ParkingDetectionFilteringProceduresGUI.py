import cv2

from ParkingDetection import ParkingDetection

from ImageHelper import ImageHelper as ih
from ImageProcessing import ProcessingGray as pg
from ImageProcessing import ProcessingColor as pc
from ImageFeaturing import FeatureDetection as fd
from ImagePreview import ImagePreview as ip
from RectSizeSelection import RectSelection


class FilteringParkingDetection(ParkingDetection):
    def detectParking(self, imagePath):

        # Load image
        img = cv2.imread(imagePath, 1)

        # Define rectangle of parking spot size - predefined dimensions
        # User defines size based on image
        rectWidth, rectHeight = self.parkingSpotSize(img)

        # Create a copy of image
        ftrImg = ih.copyImage(img)

        '''
        claColor = pc.claheColor(ftrImg)
        meanShift = pc.meanShift(ftrImg)
        gray = pc.grayScale(ftrImg)
        equ = pg.equHist(gray)
        claGray = pg.claheGray(gray)
        thresh = pg.threshOtsu(gray)
        adptThreshMean = pg.threshAdptMean(gray)
        adptThreshGauss = pg.threshAdptGauss(gray)
        dilation = pg.dilation(thresh)
        closing = pg.closing(thresh)
        canny = pg.canny(gray)
        result = canny
        '''

        # Apply median filter and mean shift filtering from processing class
        # to reduce noise and texture impact
        blur = pc.medianBlur(ftrImg)
        mean = pc.meanShift(blur)
        #colRange = pc.colorRange(mean)

        # Convert to gary and apply adaptive threshold to it
        gray = cv2.cvtColor(mean, cv2.COLOR_BGR2GRAY)
        adpThresh = pg.threshAdptGauss(gray)

        # Apply morphological gradient on thresholded image
        # to find boundaries of objects
        #res = cv2.bitwise_and(colRange, adpThresh)
        gradient = pg.gradient(adpThresh)
        #closing = pg.closing(gradient)
        result = gradient
                
        '''
        blur = pc.medianBlur(ftrImg)
        mean = pc.meanShift(blur)

        gray = cv2.cvtColor(mean, cv2.COLOR_BGR2GRAY)
        adpThresh = pg.threshAdptGauss(gray)

        opening = pg.opening(adpThresh)
        erosion = pg.erosion(opening)
        dilation = pg.dilation(erosion)
        result = opening
        '''

        '''
        blur = pc.bilateralBlur(ftrImg)
        mean = pc.meanShift(blur)
        gray = pc.grayScale(mean)

        sobelx8u = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=5)
        canny = pg.canny(sobelx8u)

        adpThresh = pg.threshAdptGauss(gray)

        res = np.bitwise_or(canny,adpThresh)
        opening = pg.opening(res)
        result = sobelx8u
        '''

        # Copy image
        dtcImg = ih.copyImage(result)

        # img = fd.drawLines(img, fd.detectLines(dtcImg))

        # Find all contours in the image
        contours = fd.detectSqrContours(dtcImg)
        # img = fd.drawBiggestContour(img, contours)
        # img = fd.drawContours(img, contours)
        # Draw only contours with parking spot dimensions +- 20% tolerance
        img = fd.drawSizedContours(img, contours, rectWidth, rectHeight, 0.2)
        # img = fd.drawRatioContours(img, contours, 2, 0.2)


        cv2.imshow('comparison', ip.stackImages(img, result))
        cv2.waitKey()
        cv2.destroyAllWindows()

        return


    # Function returns rectangle dimensions based on user input
    def parkingSpotSize(self, img):
        print "Select parking spot size and press Enter:"
        rs = RectSelection(ih.copyImage(img))
        rectWidth, rectHeight = rs.getRectSize()
        #rectWidth, rectHeight = 60, 110
        print "Parking spot size: " + str(rectWidth) + "x" + str(rectHeight)
        return rectWidth, rectHeight
