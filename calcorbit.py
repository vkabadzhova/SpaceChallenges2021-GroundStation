import pyorbital
from pyorbital.orbital import Orbital
from math import *
from datetime import datetime
import serial
import serial.tools.list_ports as listports
import time


scheduled_time = datetime.utcnow();
length = 240 # number of hours to find next passes
tol=.001 #  precision of the result in seconds
horizon = 0 # elevation of horizon to compute risetime and falltime

Re=6378.137
gela=(41.6572860, 24.5745002, 1.500)
gelaLon, gelaLat, gelaAlt = gela

sat=Orbital("QMR-KWT")
azimuth, elevation = sat.get_observer_look(scheduled_time,gelaLon, gelaLat, gelaAlt)

nextPass = sat.get_next_passes(scheduled_time, length, gelaLon, gelaLat, gelaAlt, tol=tol, horizon=horizon)
for passes in nextPass:
	for passes in passes:
		print(passes)
	print('')


port='COM4'
ports=list(listports.comports())
for p in ports:
	p=str(p)
	if 'arduino' in p.lower():
		port = p.split()[0]
		print(port)
		break
ser = serial.Serial(port, 9600)
time.sleep(.1)
# a=ser.write(input("az,el=").encode())
# print(ser.readline())
# ser.open()

def rotate(az,el):
    ser.write(f'{az},{el}'.encode())

print(azimuth,elevation)
rotate(azimuth,elevation)
