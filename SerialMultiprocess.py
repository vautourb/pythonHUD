from multiprocessing import Process

import serial
import time


class MySerialManager(Process):
    def __init__(self, serial_port, baudrate=9600, timeout=None):
        super(MySerialManager, self).__init__(target=self.loop_iterator,args=(serial_port, baudrate, timeout))


    def loop_iterator(self,serial_port, baudrate,timeout):
        ser = serial.Serial(serial_port, baudrate=baudrate, timeout=None)
        self.loop(ser)

    def loop(self,ser):

        while True:
            data_raw = ser.readline()
            print(data_raw)



if __name__ == "__main__":
    msm = MySerialManager("COM5")
    try:
        msm.start()
    except KeyboardInterrupt:
        print("caught in main")
    finally:
        msm.join()