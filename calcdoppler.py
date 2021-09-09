from math import *
import numpy as np
from datetime import datetime
import pyorbital
from pyorbital.orbital import Orbital

gela=(24.5730, 41.6500015, 1463)    # Coordinates of Gela, Bulgaria 
lon, lat, ao = gela #ao is observer altitude above sea level
sat = Orbital("QMR-KWT")
satlon,satlat, asat = sat.get_lonlatalt(datetime.utcnow()) #altitude of satellite
el = sat.get_observer_look(datetime.utcnow(),lon, lat, ao) # elevation angle towards sat
'''
def getSatVelocity(sat, utcTime): #sat = Orbital('QMR-KWT') or sth
	Vvector = sat.get_position(utcTime,0)[1] #velocity vector
	Vs = sqrt(np.sum(np.square(np.multiply(Vvector,1e3))))
	return Vs
'''
def getVectorMagnitude(v):
	return np.sqrt(np.sum(np.square(v)))

def calcReAtLat(lat): # the earth is a potato  
	r1 = 6378.14e3 #earth equatorial radius
	r2 = 6356.75e3 #earth polar radius
	#(values from https://calgary.rasc.ca/latlong.htm)
	lat = radians(lat)
	Re=sqrt(((r1**2*cos(lat))**2+(r2**2*sin(lat))**2)/((r1*cos(lat))**2+(r2*sin(lat))**2)) # (formula from https://rechneronline.de/earth-radius/ )
	return Re/1e3

def getAngleBetweenVectors(v1,v2):
	unit_v1 = v1 / np.linalg.norm(v1)
	unit_v2 = v2 / np.linalg.norm(v2)
	dot_product = np.dot(unit_v1, unit_v2)
	angle = degrees(np.arccos(dot_product))
	return angle

def calcTriangleToObserver(sat,lon,lat,alt, utc):
	satPosVector = sat.get_position(utc, 0)[0]
	satDistance = getVectorMagnitude(satPosVector) # to center of earth
	r = calcReAtLat(lat)+alt/1000
	x = r*cos(lat)*cos(lon)
	y = r*cos(lat)*sin(lon)
	z = r*sin(lat)
	observerPosVector = (x,y,z)
	observerDistance = getVectorMagnitude(observerPosVector) # to center of earth
	distanceVector = np.subtract(satPosVector, observerPosVector)
	distanceMagnitude = getVectorMagnitude(distanceVector) # from sat to observer
	return distanceMagnitude, observerDistance, satDistance, distanceVector

def getSatRelativeVelocity(sat, utc,lon,lat,alt):
	distanceMagnitude, observerDistance, satDistance, distanceVector = calcTriangleToObserver(sat,lon,lat,alt, utc)
	satPosVector, satVelocityVector = np.multiply(sat.get_position(utc, 0),1000)
	angle = getAngleBetweenVectors(satVelocityVector,distanceVector)
	velocity = getVectorMagnitude(satVelocityVector)
	relativeVelocity = velocity*cos(radians(angle))
	return relativeVelocity
'''
def calcAngleToObserver(Re,ao,asat,el): #potato radius, observer altitude, satellite altitude, elevation from horizon
	cosElPN = cos(radians(el+90)) # cos(el+90deg)
	x = (Re+ao)*cosElPN+sqrt((Re+ao)**2*(cosElPN**2)+(Re+asat)**2) #distance between sat and observer
	cosGamma = ((Re+asat)**2+(Re+ao)**2-x**2)/(2*(Re+asat)*(Re+ao)) #calculate cosine of gamma (using cosine theorem) where gamma is the angle between the observer and the satellite from the center of the earth
	gamma = acos(cosGamma) # get the angle (in radians)
	return gamma 
'''
def calcDopplerShift(f,Vsx,Vo=0): #difference in frequencies (in KHz) for stationary observer
	#frequency in MHz, 1d velocity of satellite, 1d velocity of observer 
	c=299792458#speed of light in meters
	df=f*((c+Vo)/(c+Vsx)-1)
	return df*1e3


def main():
	global el
	el = 89.9
	earth_radius = getRadiusFromLatitude(lat)
	gamma = getAngleToObserver(earth_radius, altitude_gs, altitude_sat, el)
	Vs_x = cos(getAngleToObserver(earth_radius, altitude_gs, altitude_sat, el) + np.deg2rad(el)) * getSatelliteVelocity(sat,datetime.utcnow())
	print(getDopplerShift(frequency, Vs_x),'KHz')

	h = 400e3
	earth_radius = earth_radius * 10**3
	x = getDistanceToObserver(earth_radius, 1.463, h)
	

	c = np.sqrt(2 * ((h+earth_radius) **2) - 2 * ((h+earth_radius) **2) * np.cos(gamma))

	arc = 2 * np.pi * (h+earth_radius) * (np.rad2deg(gamma) / 360)
	print("radius", earth_radius)

	v = 7.8e3

	t = arc / v

	print(arc)

	print(x, h, c)
	phi = np.arccos((x ** 2 + h ** 2 - c ** 2) / (2 * x * h)) # rad

	result = phi / t

	print(result)




if __name__ == "__main__":
    main()

