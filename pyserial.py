import serial
import time

ser = serial.Serial('COM4', 9600)
time.sleep(.1)
a=ser.write(input("az,el=").encode())
print(ser.readline())
print(ser.readline())
# print(ser.readline())
# ser.open()
