import pyorbital
from pyorbital.orbital import Orbital
from math import *
from datetime import datetime, timedelta
import serial
import sys
import glob
import serial.tools.list_ports as listports
import time
from django import template


gela=( 24.5730,41.6500015, 1.463)    # Coordinates of Gela, Bulgaria 
gelaLon, gelaLat, gelaAlt = gela


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def norad_to_name(norad_id):
	if type(norad_id) == type('some string'):
		if norad_id.isdigit():
			norad_id = int(norad_id)
		else:
			return norad_id
	tlefile_lines=open('tle.txt').read().split('\n')
	for i in range(len(tlefile_lines)):
	 	line = tlefile_lines[i]
	 	if len(line) <= 0 or not line[0] == '1':
	 		continue
	 	tle_norad_id = line.split(' ')[1][:-1]
	 	if tle_norad_id == str(norad_id):
	 		sat_name = tlefile_lines[i-2].strip()
	 		return sat_name

# def get_next_coordinates(sat_name='QMR-KWT', tle_file=None, scheduled_time=datetime.utcnow(), length=240, tolerance=.001, horizon=0):
def get_next_sat_coordinates(sat_name='QMR-KWT', scheduled_time=datetime.utcnow(), length=2, tolerance=.001, horizon=0):
	"""Calculate next step for the rotator

		:scheduled_time: Satellite's tracking starting time
		:length: Number of hours to find next passes
		:tolerance: Precision of the result in seconds
		:horizon: Elevation of horizon to compute risetme and falltime
		:return: Angles for the Arduino rotator - azimuth, elevation 
	"""
	# sat_name = norad_to_name(sat_name) if type(sat_name) == type(1) else sat_name
	Re=6378.137                             # Earth's radius
	gela=( 24.5730,41.6500015, 1.463)    # Coordinates of Gela, Bulgaria 
	gelaLon, gelaLat, gelaAlt = gela

	realtime = False
	if scheduled_time == datetime.utcnow():
		realtime = True

	sat=Orbital(sat_name, "tle.txt")
	#get az and el towards satellite

	azimuth, elevation = sat.get_observer_look(datetime.utcnow() if realtime else scheduled_time,gelaLon, gelaLat, gelaAlt)

	#print rise, max elevation and set time of next passes in the next <length> hours
	"""
	nextPass = sat.get_next_passes(scheduled_time, length, gelaLon, gelaLat, gelaAlt, tol=tolerance, horizon=horizon)
    for passes in nextPass:
		for passes in passes:
			print(passes)
		print('')
	"""
	return azimuth, elevation

def get_next_passes_info(sat_name, lon=gelaLon,lat=gelaLat,alt=gelaLat,hours=72,horizon=15, tolerance=.001):
	sat = Orbital(sat_name,"tle.txt")
	passes = sat.get_next_passes(datetime.utcnow(), hours, lon, lat, alt, tolerance, horizon)
	info=[]
	for p in passes:
		apogee = sat.get_observer_look(p[2], lon, lat, alt)[1]
		info.append(((p[0]+timedelta(hours=3)).strftime("%d.%m"),(p[0]+timedelta(hours=3)).strftime("%H:%M"),(p[1]+timedelta(hours=3)).strftime("%H:%M"),apogee))
	return info

def init_arduino_serial_connection(port="COM8"):
	"""
		Realize serial communication with the Arduino  
	"""

			
	ser = serial.Serial(port, 19200)
	time.sleep(.1) # small delay is needed
	return ser


def rotate(ser, az, el): #send str to serial from two nums; ex. output: b'124.40,-34.18'
	message = 'AZ{} EL{}\n'.format(az, el).encode()
	print(message)
	if ser is not None:
		ser.write(message)
