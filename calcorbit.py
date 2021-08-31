import pyorbital
from pyorbital.orbital import Orbital
from math import *
from datetime import datetime
import serial
import serial.tools.list_ports as listports
import time


# def get_next_coordinates(sat_name='QMR-KWT', tle_file=None, scheduled_time=datetime.utcnow(), length=240, tolerance=.001, horizon=0):
def get_next_sat_coordinates(sat_name='QMR-KWT', scheduled_time=datetime.utcnow(), length=240, tolerance=.001, horizon=0):
	"""Calculate next step for the rotator

		:scheduled_time: Satellite's tracking starting time
		:length: Number of hours to find next passes
		:tolerance: Precision of the result in seconds
		:horizon: Elevation of horizon to compute risetme and falltime
		:return: Angles for the Arduino rotator - azimuth, elevation 
	"""

	Re=6378.137                             # Earth's radius
	gela=(24.5730, 41.6500015, 1.463)    # Coordinates of Gela, Bulgaria 
	gelaLon, gelaLat, gelaAlt = gela

	sat=Orbital(sat_name, "tle.txt")
	#get az and el towards satellite
	azimuth, elevation = sat.get_observer_look(scheduled_time,gelaLon, gelaLat, gelaAlt)

	#print rise, max elevation and set time of next passes in the next <length> hours
	"""
	nextPass = sat.get_next_passes(scheduled_time, length, gelaLon, gelaLat, gelaAlt, tol=tolerance, horizon=horizon)
    for passes in nextPass:
		for passes in passes:
			print(passes)
		print('')
	"""
	return azimuth, elevation
	


def init_arduino_serial_connection():
	"""
		Realize serial communication with the Arduino  
	"""
	
	port='COM4' #default port
	
	#detect arduino port
	ports=list(listports.comports())
	for p in ports:
		p=str(p)
		if 'arduino' in p.lower():
			port = p.split()[0]
			print(port)
			break
			
	ser = serial.Serial(port, 9600)
	time.sleep(.1) # does not work without the delay
	return ser


def rotate(ser, az, el): #send str to serial from two nums; ex. output: b'124.40,-34.18'
	ser.write(f'{az},{el}'.encode())


def init_tracking(sat_name, reservation_datetime):
    azimuth, elevation = get_next_sat_coordinates(sat_name)
    # ser = init_arduino_serial_connection()

    print(azimuth,elevation)
    # rotate(ser, azimuth, elevation)
