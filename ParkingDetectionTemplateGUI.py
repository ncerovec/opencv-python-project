import cv2
import numpy as np

from ParkingDetection import ParkingDetection

class TemplateParkingDetection(ParkingDetection):
    def detectParking(self, imgPath, templatePath):

        # Load the image and template
        img = cv2.imread(imgPath)

        template = cv2.imread(templatePath, 1)

        # Bilateral blur on image to preserve edges but reduce noise
        img_blur = cv2.bilateralFilter(img, 9, 75, 75)

        # Mean shift filtering to reduce texture effect
        img_mean = cv2.pyrMeanShiftFiltering(img_blur, 30, 20, 3)

        # Convert to grayscale
        img_gray = cv2.cvtColor(img_mean, cv2.COLOR_BGR2GRAY)

        # Calculate median of image and apply canny filter with thresholds based on median
        img_median_val = np.median(img_gray)
        sigma = 0.33
        lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
        upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
        img_canny = cv2.Canny(img_gray, lower_thresh, upper_thresh)

        # Use adaptive threshold also based on median to extract as much cars possible
        img_adaptive = cv2.adaptiveThreshold(img_gray, img_median_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 13, -1)
        # Brighten the result
        img_adaptive = cv2.equalizeHist(img_adaptive)

        # To get clean edges with add canny and adaptive result together
        img_canny_adaptive = np.bitwise_or(img_canny, img_adaptive)

        # Apply opening to try closing some shapes
        kernel = np.ones((2, 2), np.uint8)
        img_opening = cv2.morphologyEx(img_canny_adaptive, cv2.MORPH_OPEN, kernel)

        # Apply canny on template to detect edges
        template_canny = cv2.Canny(template, 50, 100)

        # Find contours on template based on edges
        contours_template, hierarchy = cv2.findContours(template_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours by minimal area
        # For each contour on template define ROI and extract it on proccesed image
        # Inspect and decide based on average if the sport is taken
        contour_area_min = 100
        for contour in contours_template:
            if cv2.contourArea(contour) > contour_area_min:
                x, y, w, h = cv2.boundingRect(contour)
                roi = img_opening[y:y + h, x:x + w]
                roi_average = np.average(roi)
                if (roi_average > 30):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

        cv2.imshow("Result", img)

        cv2.waitKey()
        cv2.destroyAllWindows()

        return
