import pyorbital
from pyorbital.orbital import Orbital
from math import *
from datetime import datetime
import serial
import sys
import glob
import serial.tools.list_ports as listports
import time


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

# def get_next_coordinates(sat_name='QMR-KWT', tle_file=None, scheduled_time=datetime.utcnow(), length=240, tolerance=.001, horizon=0):
def get_next_sat_coordinates(sat_name='QMR-KWT', scheduled_time=datetime.utcnow(), length=2, tolerance=.001, horizon=0):
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
	azimuth, elevation = sat.get_observer_look(scheduled_time, gelaLon, gelaLat, gelaAlt)

	#print rise, max elevation and set time of next passes in the next <length> hours
	"""
	nextPass = sat.get_next_passes(scheduled_time, length, gelaLon, gelaLat, gelaAlt, tol=tolerance, horizon=horizon)
    for passes in nextPass:
		for passes in passes:
			print(passes)
		print('')
	"""
	return azimuth, elevation
	


def init_arduino_serial_connection(port="COM8"):
	"""
		Realize serial communication with the Arduino  
	"""

			
	ser = serial.Serial(port, 19200)
	time.sleep(.1) # small delay is needed
	return ser


def rotate(ser, az, el): #send str to serial from two nums; ex. output: b'124.40,-34.18'
	message = 'AZ{} EL{}'.format(az, el).encode()
	print(message)
	ser.write(message)

def main():
	port = serial_ports()
	ser = init_arduino_serial_connection(port[0])

	while(True):
		sat_name = "QMR-KWT"
		time_now = datetime.utcnow()
		azimuth, elevation = get_next_sat_coordinates(sat_name, time_now)
		az = ('%.1f') % azimuth
		el = ('%.1f') % elevation
		rotate(ser, az, el)
		time.sleep(10)

if __name__ == "__main__":
	main()