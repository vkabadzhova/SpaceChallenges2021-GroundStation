from math import *
import numpy as np
from datetime import datetime
import pyorbital
from pyorbital.orbital import Orbital

gela=(24.5730, 41.6500015, 1463)    # Coordinates of Gela, Bulgaria 
lon, lat, altitude_gs = gela # altitude_gs is observer altitude above sea level
sat = Orbital("QMR-KWT")
satlon, satlat, altitude_sat = sat.get_lonlatalt(datetime.utcnow()) #altitude of satellite
az, el = sat.get_observer_look(datetime.utcnow(),lon, lat, altitude_gs) # elevation angle towards sat
frequency = 436.5

def getSatelliteVelocity(sat, utcTime): #sat = Orbital('QMR-KWT') or sth
	Vvector = sat.get_position(utcTime,0)[1] #velocity vector
	Vs = sqrt(np.sum(np.square(np.multiply(Vvector,1e3))))
	return Vs

def getRadiusFromLatitude(lat): # the earth is a potato  
	r1 = 6378.14e3 #earth equatorial radius
	r2 = 6356.75e3 #earth polar radius
	# (values from https://calgary.rasc.ca/latlong.htm)
	lat = radians(lat)
	earth_radius = sqrt(((r1**2*cos(lat))**2+(r2**2*sin(lat))**2)/((r1*cos(lat))**2+(r2*sin(lat))**2)) # (formula from https://rechneronline.de/earth-radius/ )
	return earth_radius / 1e3

def getDistanceToObserver(earth_radius, altitude_gs, altitude_sat):
	cosElPN = cos(radians(el+90)) # cos(el+90deg)
	x = (earth_radius+altitude_gs)*cosElPN+sqrt((earth_radius+altitude_gs)**2*(cosElPN**2)+(earth_radius+altitude_sat)**2) #distance between sat and observer
	return x

def getAngleToObserver(earth_radius, altitude_gs, altitude_sat, el): #potato radius, observer altitude, satellite altitude, elevation from horizon
	cosElPN = cos(radians(el+90)) # cos(el+90deg)
	x = (earth_radius+altitude_gs)*cosElPN+sqrt((earth_radius+altitude_gs)**2*(cosElPN**2)+(earth_radius+altitude_sat)**2) #distance between sat and observer
	cosGamma = ((earth_radius+altitude_sat)**2+(earth_radius+altitude_gs)**2-x**2)/(2*(earth_radius+altitude_sat)*(earth_radius+altitude_gs)) #calculate cosine of gamma (using cosine theorem) where gamma is the angle between the observer and the satellite from the center of the earth
	gamma = acos(cosGamma) # get the angle (in radians)
	return gamma

def getDopplerShift(f,Vsx,Vo=0): #difference in frequencies (in KHz) for stationary observer
	# frequency in MHz, 1d velocity of satellite, 1d velocity of observer 
	c = 299792458 # speed of light in meters per sec
	df=f*((c+Vo)/(c+Vsx)-1)
	return df*1e3


def main():
	earth_radius = getRadiusFromLatitude(lat)
	gamma = getAngleToObserver(earth_radius, altitude_gs, altitude_sat, el)
	Vs_x = cos(getAngleToObserver(earth_radius, altitude_gs, altitude_sat, el) + np.deg2rad(el)) * getSatelliteVelocity(sat,datetime.utcnow())
	print(getDopplerShift(frequency, Vs_x),'KHz')

if __name__ == "__main__":
    main()

