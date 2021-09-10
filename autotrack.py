import calcorbit as co
import time 
from datetime import datetime, timedelta
from serial.tools import list_ports
import serial
import pyorbital
from pyorbital import orbital

gela=( 24.5730,41.6500015, 1.463)    # Coordinates of Gela, Bulgaria 
gelaLon, gelaLat, gelaAlt = gela


try:
	port = [x for x in list(serial.tools.list_ports.comports())[0] if 'COM' in x][0]
	ser = serial.Serial(port, 9600)
	time.sleep(.1) # does not work without the delay
except:
	print('no serial ports available')

# pyorbital.tlefile.fetch('tle.txt')
while 1:
	name = co.norad_to_name(input("Sat Name: "))
	print(name)
	try:
		az,el = co.get_next_sat_coordinates(name,datetime.utcnow())
		az=az if az <=180 else 360-az
	except:
		print("sat not found")
		continue 
	if(el>0):
		try:
			print("apogey time:",str(orbital.Orbital(name,tle_file="tle.txt").get_next_passes(datetime.utcnow()-timedelta(hours=12), 12, gelaLon, gelaLat, gelaAlt)[-1][2]+timedelta(hours=3))[11:19])
			print("setting time:",str(orbital.Orbital(name,tle_file="tle.txt").get_next_passes(datetime.utcnow()-timedelta(hours=12), 12, gelaLon, gelaLat, gelaAlt)[-1][1]+timedelta(hours=3))[11:19])
		except:
			pass
	while el > 0:
		az,el = co.get_next_sat_coordinates(name,datetime.utcnow())
		az=az if az <=180 else 360-az
		s=f'AZ{round(-az,1)} EL{round(el,1)}\n'.encode()
		print(round(az,1), round(el,1))
		ser.write(s)
		time.sleep(1)

	print("sat is below horizon")
	print("rising time:",str(orbital.Orbital(name,tle_file="tle.txt").get_next_passes(datetime.utcnow(), 12, gelaLon, gelaLat, gelaAlt)[0][0]+timedelta(hours=3))[11:19])
	print("apogey time:",str(orbital.Orbital(name,tle_file="tle.txt").get_next_passes(datetime.utcnow(), 12, gelaLon, gelaLat, gelaAlt)[0][2]+timedelta(hours=3))[11:19])
	print("setting time:",str(orbital.Orbital(name,tle_file="tle.txt").get_next_passes(datetime.utcnow(), 12, gelaLon, gelaLat, gelaAlt)[0][1]+timedelta(hours=3))[11:19])
	print("max elevation",orbital.Orbital(name,tle_file="tle.txt").get_observer_look(orbital.Orbital(name,tle_file="tle.txt").get_next_passes(datetime.utcnow(), 12, gelaLon, gelaLat, gelaAlt)[0][2], gelaLon, gelaLat, gelaAlt)[1])
# input('press any key to exit')