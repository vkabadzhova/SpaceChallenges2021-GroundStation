import pyorbital
from pyorbital.orbital import Orbital
from math import *
from datetime import datetime
import serial
import serial.tools.list_ports as listports
import time

def print_next_passes(sat_name='QMR-KWT', scheduled_time=datetime.utcnow(), length=240, tolerance=.001, horizon=0):
    """Calculate next step for the rotator

        :scheduled_time: Satellite's tracking starting time
        :length: Number of hours to find next passes
        :tolerance: Precision of the result in seconds
        :horizon: Elevation of horizon to compute risetme and falltime
        :return: Angles for the Arduino rotator - azimuth, elevation 
    """

    Re=6378.137                             # Earth's radius
    gela=(41.6572860, 24.5745002, 1.500)    # Coordinates of Gela, Bulgaria 
    gelaLon, gelaLat, gelaAlt = gela

    sat=Orbital(sat_name)
    azimuth, elevation = sat.get_observer_look(scheduled_time,gelaLon, gelaLat, gelaAlt)

    nextPass = sat.get_next_passes(scheduled_time, length, gelaLon, gelaLat, gelaAlt, tol=tol, horizon=horizon)
    for passes in nextPass:
	for passes in passes:
		print(passes)
	print('')

def serial_connect_arduino():
    """
        Realize serial communication with the Arduino  
    """
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
