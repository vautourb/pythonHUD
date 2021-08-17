from multiprocessing import Process

import datetime
import cv2
import threading
import serial
import webview

longitude = 0
latitude = 0
cur_speed = 0
miniMapurl = 'https://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(longitude) + '&zoom=18&size=512x512&maptype=hybrid&key=AIzaSyDg0SwqnAZuPSr86Z8XlJk65atfFqLvAjw'


def miniMap(window):
    global miniMapurl
    window = webview.create_window(miniMapurl, x=3075, y=1450, width=512, height=512, on_top=True, frameless=True)


#window = webview.create_window(miniMapurl, x=3075, y=1450, width=512, height=512, on_top=True, frameless=True)
webview.start(miniMap, window)
# anything below this line will be executed after program is finished executing
pass


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
        cv2.putText(frame, 'LON :' + " " +  str(longitude), (5, 20), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LAT :' + " "+  str(latitude), (5, 40), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SPD :' + " "+  str(cur_speed), (5, 60), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        # cv2.putText(frame, 'BRG :' + " ",+  str(global_brg) (5, 80), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create threads as follows
# overlay Thermal Cam onto IR cam work on that later Get all Cams Working First

class myGPSThread(threading.Thread):

    def __init__(self, serial_port, baud_rate):

        self.ser = serial.Serial(port=self.serial_port, baudrate=self.baud_rate)
        self.port = "COM5"
        self.baudrate = 9600

    def run(self):
        print( "Starting GPS")
        self.end_event.set()

    def get_gps_data(self):
        self.gpsStr = self.ser.readline()
        gps = None

        try:
            # gps = serial.Serial(self.ser)
            ser_bytes = self.ser.readline()
            decoded_bytes = ser_bytes.decode("utf-8")
            data = decoded_bytes.split(",")

            if data[0] == '$GPRMC':
                # print(data)
                # Convert NMEA to Decimal
                lat_nmea = data[3]
                lat_degrees = lat_nmea[:2]
                if data[4] == 'S':
                   latitude_degrees = float(lat_degrees) * -1
                else:
                    latitude_degrees = float(lat_degrees)
                    # Change it back to a string and remove the .0
                    latitude_degrees = str(latitude_degrees).strip('.0')
                    lat_ddd = lat_nmea[2:10]
                    lat_mmm = float(lat_ddd) / 60
                    lat_mmm = str(lat_mmm).strip('0.')[:8]
                    latitude = latitude_degrees + "." + lat_mmm
                        # Convert Longitude to decimal Coordinates
                    long_nmea = data[5]
                    long_degrees = long_nmea[1:3]
                    if data[6] == 'W':
                        longitude_degrees = float(long_degrees) * -1
                    else:
                        longitude_degrees = float(long_degrees)
                        # Change it back to a string and remove the .0
                    longitude_degrees = str(longitude_degrees).strip('.0')
                    long_ddd = long_nmea[3:10]
                    long_mmm = float(long_ddd) / 60
                    long_mmm = str(long_mmm).strip('0.')[:8]
                    longitude = longitude_degrees + "." + long_mmm

                    speed_nmea = data[7]
                    speed_kmh = float(speed_nmea) * 1.852
                    cur_speed = str(speed_kmh)

                    print("Longitude : " + longitude + "°" + data[6] + " Latitude : " + latitude + "°" + data[4] + " Spd  : " + cur_speed + " Kmh")

  #      global_longitude = longitude
  #      global_latitude = latitude
  #      global_cur_speed = cur_speed
            return longitude, latitude, cur_speed

        except serial.SerialException:
            print("There is no GPS Device Connected to this computer.")

            return longitude, longitude, cur_speed
        finally:
            if gps is not None:
                gps.close()



# multiprocessing actually uses separate processes,
# you cannot simply share global variables because they will be in completely
# different "spaces" in memory. What you do to a global under one process will
# not reflect in another. Though I admit that it seems confusing since the way
# you see it, its all living right there in the same piece of code, so
# "why shouldn't those methods have access to the global"?
# Its harder to wrap your head around the idea that they will be running in
# different processes.

# The Manager class is given to act as a proxy for data structures
# that can shuttle info back and forth for you between processes.
# What you will do is create a special dict and list from a manager,
# pass them into your methods, and operate on them locally.


thread1 = camThread("Main Cam", 0)  # Primary Camera
thread2 = camThread("IR Cam", 1)  # IR Camera
thread3 = camThread("Thermal Cam", 2)  # Thermal Camera
thread4 = camThread("NV Cam", 3)  # Night Vision Camera
thread5 = myGPSThread("GPS collection",)

#  UNCOMMENT TO START THREADS
thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
thread5.start()
print()
print("Active threads", threading.activeCount())
