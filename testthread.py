import threading
import cv2
import datetime



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
    cam = cv2.VideoCapture(camID, cv2.CAP_DSHOW)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        font = cv2.FONT_HERSHEY_DUPLEX
        today = datetime.datetime.now()
        date_time = today.strftime("%m/%d/%Y   %H:%M:%S.%f")[:-4]
        cv2.putText(frame, date_time, (225, 475), font, .3, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LON :' + " ", (5, 20), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LAT :' + " ", (5, 40), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'BRG :' + " ", (5, 60), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SPD :' + " ", (5, 80), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)
    print()
    print("Active threads", threading.activeCount())


threadLock = threading.Lock()
threads = []

# Create new threads
#thread1 = HUDThread("Thread-1", 1)
#thread2 = HUDThread("Thread-2", 2)
#thread3 = HUDThread("Thread-GPS", 3)
thread4 = camThread("Main Cam", 0)  # Primary Camera
thread5 = camThread("IR Cam", 1)  # IR Camera
thread6 = camThread("Thermal Cam", 2)  # Thermal Camera
thread7 = camThread("NV Cam", 3)  # Night Vision Camera

# Start new Threads
#thread1.start()
# thread2.start()
#thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()


# Add threads to thread list
#threads.append(thread1)
#threads.append(thread2)
#threads.append(thread3)
threads.append(thread4)
threads.append(thread5)
threads.append(thread6)
threads.append(thread7)

# Wait for all threads to complete

