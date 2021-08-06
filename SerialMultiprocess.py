from multiprocessing import Process

import serial
import time

global_longitude = 0
global_latitude = 0
global_cur_speed = 0


class MySerialManager(Process):
    def __init__(self, serial_port, baudrate=9600, timeout=None):
        super(MySerialManager, self).__init__(target=self.loop_iterator, args=(serial_port, baudrate, timeout))

    def loop_iterator(self, serial_port, baudrate, timeout):
        ser = serial.Serial(serial_port, baudrate=baudrate, timeout=None)
        self.loop(ser)

    def loop(self, ser):

        while True:
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
                    cur_speed = str(speed_kmh)

                    print("Longitude : " + longitude + "°" + data[6] + " Latitude : " + latitude + "°" + data[
                        4] + " Spd  : " + cur_speed + " Kmh")

                #      global_longitude = longitude
                #      global_latitude = latitude
                #      global_cur_speed = cur_speed
            return longitude, latitude, cur_speed


if __name__ == "__main__":
    msm = MySerialManager("COM5")
    try:
        msm.start()
    except KeyboardInterrupt:
        print("caught in main")
    finally:
        msm.join()
