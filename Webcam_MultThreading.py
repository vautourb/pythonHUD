import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create threads as follows
thread1 = camThread("Camera 1", 0)   # Primary Camera
thread2 = camThread("Camera 2", 1)  # IR Camera
thread3 = camThread("Camera 3", 2)  # Thermal Camera
thread4 = camThread("Camera 4", 3)  # Night Vision Camera

thread1.start()
thread2.start()
thread3.start()
thread4.start()
print()
print("Active threads", threading.activeCount())
