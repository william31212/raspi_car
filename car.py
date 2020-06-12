#!/usr/bin/env python3
import serial
from time import sleep
import struct

class Car:
    Forward = 0
    Backward = 1

    def __init__(self, device, baud_rate, timeout=1):
        self.serial = serial.Serial(device, baud_rate, timeout=timeout)
        self.serial.flush()
    def __del__(self):
        self.serial.flush()
        self.serial.close()

    def go(self, ldir, lspeed, rdir, rspeed):
        assert lspeed >= 0 and lspeed <= 255
        assert rspeed >= 0 and rspeed <= 255
        dir_char = {Car.Forward: b'+', Car.Backward: b'-'}
        inc = dir_char[ldir] + struct.pack('B', lspeed) + dir_char[rdir] + struct.pack('B', rspeed)
        self.serial.flush()
        self.serial.write(inc)
        msg = self.serial.readline()
        # print(msg)

    def stop(self):
        self.go(Car.Forward, 0, Car.Forward, 0)        

    def go_forward(self, speed):
        self.go(Car.Forward, speed, Car.Forward, speed)

    def go_backward(self, speed):
        self.go(Car.Backward, speed, Car.Backward, speed)

    def go_left(self, speed):
        self.go(Car.Backward, speed, Car.Forward, speed)

    def go_right(self, speed):
        self.go(Car.Forward, speed, Car.Backward, speed)

# Example
# car = Car('/dev/ttyACM0', 9600)

# car.go_forward(100)
# sleep(1)
# car.stop()

# car.go_backward(100)
# sleep(1)
# car.stop()

# car.go_left(100)
# sleep(1)
# car.stop()

# car.go_right(100)
# sleep(1)
# car.stop()