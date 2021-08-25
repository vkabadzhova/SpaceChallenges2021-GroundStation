import pyorbital
from pyorbital.orbital import Orbital
from math import *
from datetime import datetime
import serial
import serial.tools.list_ports as listports
import time


scheduled_time = datetime.utcnow();
length = 240 # number of hours to find next passes
precision=.001 #  precision of the result in seconds
horizon = 0 # elevation of horizon to compute risetime and falltime

Re=6378.137
gela=(41.6572860, 24.5745002, 1.500) #lon lat alt in km
gelaLon, gelaLat, gelaAlt = gela

sat=Orbital("QMR-KWT") #should be based on satellite name

#get az and el towards satellite
azimuth, elevation = sat.get_observer_look(scheduled_time,gelaLon, gelaLat, gelaAlt)

#print rise, max elevation and set time of next passes in the next <length> hours
nextPass = sat.get_next_passes(scheduled_time, length, gelaLon, gelaLat, gelaAlt, tol=precision, horizon=horizon)
for passes in nextPass:
	for passes in passes:
		print(passes)
	print('')


port='COM4' #default port
#detect arduino port
ports=list(listports.comports())
if len(ports) == 0:
	
for p in ports:
	p=str(p)
	if 'arduino' in p.lower():
		port = p.split()[0]
		print(port)
		break
ser = serial.Serial(port, 9600)
time.sleep(.1) #for some reason it doesnt work without this delay

def rotate(az,el): #send str to serial from two nums; ex. output: b'124.40,-34.18'
    ser.write(f'{az},{el}'.encode())

print(azimuth,elevation)
rotate(azimuth,elevation)
