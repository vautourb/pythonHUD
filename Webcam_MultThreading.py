import datetime
import cv2
import threading
import serial
import serial.tools.list_ports

# Serial port variables
# AutoDetect Comports and Print Port name and Device Connected
print('Searching for COM Ports...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports:
    print('Found port : ' + port.device + " : Details : " + str(port) + " : " + str(port.pid))
baud = 9600
serial_port = serial.Serial(port.device, baud, timeout=0)

#GPS Variables
latitude = 0
longitude = 0
cur_speed = 0
satLock = 0
LongitudeDegrees = 0
LatitudeDegrees = 0



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
        cv2.putText(frame, date_time, (225, 475), font, .4, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LON :' + " " + str(longitude) + " " + str(LongitudeDegrees), (5, 20), font, .4, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LAT :' + " " + str(latitude) + " " + str(LatitudeDegrees), (5, 40), font, .4, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SAT :' + " " + str(satLock), (5, 60), font, .4, (0, 255, 255), 1, cv2.LINE_AA)
        # cv2.putText(frame, 'SPD :' + " " + str(cur_speed), (5, 80), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create serial threads as follows
class serThread(threading.Thread):
    # Create a thread for each serial port
    def __init__(self, serName, serID):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.serName = serName
        self.serID = serID
    # Open Available Serial Ports

    def run(self):
        print("Starting " + self.serName)
        self.lock.acquire()
        read_from_port(serial_port)
        self.lock.release()


def read_from_port(ser, ):
    while True:

        global longitude
        global latitude
        global cur_speed
        global satLock
        global LongitudeDegrees
        global LatitudeDegrees

        try:

            ser_bytes = ser.readline()
            decoded_bytes = ser_bytes.decode("utf-8")
            data = decoded_bytes.split(",")

            if data[0] == '$GPRMC':
                print("Received From COM5")
                print(data)
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
                    cur_speed = '{0:.1f}'.format(speed_kmh)

                    satLock = data[2]
                    LongitudeDegrees = data[6]
                    LatitudeDegrees = data[4]

                    print()
                    print("Active threads", threading.activeCount())
                    print("Sat Lock : " + satLock + " " + "Longitude : " + longitude + "°" + data[
                        6] + " Latitude : " + latitude + "°" + data[
                              4] + " Spd  : " + str(cur_speed) + " Km/h")
                    print()
        except:
            print()
            print("Active threads", threading.activeCount())
            print("Lost Signal")

# Camera Threads


thread1 = camThread("Main Cam", 0)  # Primary Camera
thread2 = camThread("IR Cam", 1)  # IR Camera
thread3 = camThread("Thermal Cam", 2)  # Thermal Camera
thread4 = camThread("NV Cam", 3)  # Night Vision Camera

# Serial Port Threads
thread5 = serThread("USB GPS", serial_port)
thread5.setDaemon(True)


# Camera Threads Start
thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()

# Serial Port Threads Start
thread5.start()


# test threading
print()
print("Active threads", threading.activeCount())
print()
