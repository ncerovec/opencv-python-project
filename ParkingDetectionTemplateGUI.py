import cv2
import numpy as np

from ParkingDetection import ParkingDetection


def find_if_close(cnt1, cnt2):
    row1, row2 = cnt1.shape[0], cnt2.shape[0]
    for i in xrange(row1):
        for j in xrange(row2):
            dist = np.linalg.norm(cnt1[i] - cnt2[j])
            if abs(dist) < 2:
                return True
            elif i == row1 - 1 and j == row2 - 1:
                return False

class TemplateParkingDetection(ParkingDetection):
    def detectParking(self, imgPath, templatePath):

        img = cv2.imread(imgPath)

        template = cv2.imread(templatePath, 0)

        img_blur = cv2.bilateralFilter(img, 9, 75, 75)

        img_mean = cv2.pyrMeanShiftFiltering(img_blur, 30, 20, 3)

        img_gray = cv2.cvtColor(img_mean, cv2.COLOR_BGR2GRAY)

        img_median_val = np.median(img_gray)
        sigma = 0.33
        lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
        upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
        img_canny = cv2.Canny(img_gray, lower_thresh, upper_thresh)

        img_adaptive = cv2.adaptiveThreshold(img_gray, img_median_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 13, -1)
        img_adaptive = cv2.equalizeHist(img_adaptive)

        img_canny_adaptive = np.bitwise_or(img_canny, img_adaptive)

        kernel = np.ones((2, 2), np.uint8)
        img_opening = cv2.morphologyEx(img_canny_adaptive, cv2.MORPH_OPEN, kernel)

        result = cv2.bitwise_and(img_opening, template)

        contours_raw, hierarchy = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours_filtered= []
        contour_area_min = 20
        for contour in contours_raw:
            x, y, w, h = cv2.boundingRect(contour)
            if (cv2.contourArea(contour) > contour_area_min):
                contours_filtered.append(contour)


        cv2.drawContours(img, contours_filtered, -1, (0, 255, 0), 2)

        cv2.imshow("Result", img)

        cv2.waitKey()
        cv2.destroyAllWindows()

        return