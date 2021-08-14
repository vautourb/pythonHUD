import threading
import serial
import csv

connected = False
port = 'COM5'
baud = 9600

serial_port = serial.Serial(port, baud, timeout=0)


class serThread(threading.Thread):
    # Create a thread for each camera
    def __init__(self, serName, serID):
        threading.Thread.__init__(self)
        self.serName = serName
        self.serID = serID
    # Open Available Cameras

    def run(self):
        print("Starting " + self.serName)
        read_from_port(serial_port)

#def handle_data(data):
#    print(data)


def read_from_port(ser):
    while True:
        try:

            ser_bytes = ser.readline()
            decoded_bytes = ser_bytes.decode("utf-8")
            data = decoded_bytes.split(",")
            if data[0] == '$GPRMC':
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

                    #with open('GPSLog.csv', 'w+') as GPSout:
                        #thewriter = csv.writer(GPSout)
                        #thewriter.writerow(longitude, latitude, cur_speed)
                        #GPSout.flush()
                    print("Active threads", threading.activeCount())
                    print("Sat Lock : " + satLock + " " + "Longitude : " + longitude + "°" + data[
                        6] + " Latitude : " + latitude + "°" + data[
                              4] + " Spd  : " + str(cur_speed) + " Km/h")
        except:
            print("Lost Signal")


thread = serThread("USB GPS", serial_port)
# thread = threading.Thread("USB GPS", target=serThread, args=(serial_port,))
thread.start()
