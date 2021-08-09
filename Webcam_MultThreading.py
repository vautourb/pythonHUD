import datetime
import cv2
import threading


class camThread(threading.Thread):
    # Create a thread for each camera
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    # Open Available Cameras

    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

# Show Cameras on Display and Process any edits to the stream


def camPreview(previewName, camID):
    cv2.namedWindow(previewName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(previewName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        font = cv2.FONT_HERSHEY_DUPLEX
        today = datetime.datetime.now()
        date_time = today.strftime("%m/%d/%Y, %H:%M:%S.%f")[:-4]
        cv2.putText(frame, date_time, (225, 475), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LON :' + " ", (5, 25), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LAT :' + " ", (5, 45), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'BRG :' + " ", (5, 65), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SPD :' + " ", (5, 85), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create threads as follows


thread1 = camThread("Camera 1", 0)  # Primary Camera
thread2 = camThread("Camera 2", 1)  # IR Camera
thread3 = camThread("Camera 3", 2)  # Thermal Camera
thread4 = camThread("Camera 4", 3)  # Night Vision Camera

#  uNCOMMENT TO START THREADSSStart Threads
thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
print()
print("Active threads", threading.activeCount())
