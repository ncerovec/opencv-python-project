import cv2


class FrameCapture():
    def __init__(self, deviceID):
        self.device_id = deviceID

    def captureImage(self, fileName):

        camera = cv2.VideoCapture(self.device_id)

        while (True):
            ret, frame = camera.read()

            cv2.imshow("Video Capture", frame)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite(fileName, frame)
                returnVal = 1
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                returnVal = 0
                break

        camera.release()
        cv2.destroyAllWindows()
        return returnVal
