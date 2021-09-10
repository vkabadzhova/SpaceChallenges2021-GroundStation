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

def getReAtLat(lat): # the earth is a potato  
	r1 = 6378.14e3 #earth equatorial radius
	r2 = 6356.75e3 #earth polar radius
	#(values from https://calgary.rasc.ca/latlong.htm)
	lat = radians(lat)
	Re=sqrt(((r1**2*cos(lat))**2+(r2**2*sin(lat))**2)/((r1*cos(lat))**2+(r2*sin(lat))**2)) # (formula from https://rechneronline.de/earth-radius/ )
	return Re/1e3

def getVelocityFromAngular(sat,lon, lat,alt,angularVelocity):
	r=getReAtLat(lat)
	velocityMagnitude = angularVelocity*(r+alt)*cos(lat)
	velocityVector = (velocityMagnitude*cos(radians(lon)), velocityMagnitude*sin(radians(lon)),0)
	return velocityVector


def getAngleBetweenVectors(v1,v2):
	unit_v1 = v1 / np.linalg.norm(v1)
	unit_v2 = v2 / np.linalg.norm(v2)
	dot_product = np.dot(unit_v1, unit_v2)
	angle = degrees(np.arccos(dot_product))
	return angle

def getTriangleToObserver(sat,lon,lat,alt, utc):
	satPosVector = sat.get_position(utc, 0)[0]
	satDistance = getVectorMagnitude(satPosVector) # to center of earth
	r = getReAtLat(lat)+alt/1000
	x = r*cos(lat)*cos(lon)
	y = r*cos(lat)*sin(lon)
	z = r*sin(lat)
	observerPosVector = (x,y,z)
	observerDistance = getVectorMagnitude(observerPosVector) # to center of earth
	distanceVector = np.subtract(satPosVector, observerPosVector)
	distanceMagnitude = getVectorMagnitude(distanceVector) # from sat to observer
	return distanceMagnitude, observerDistance, satDistance, distanceVector

def getSatRelativeVelocity(sat, utc,lon,lat,alt, angularVelocity = 7.292124e-5):
	distanceMagnitude, observerDistance, satDistance, distanceVector = getTriangleToObserver(sat,lon,lat,alt, utc)
	satPosVector, satVelocityVector = np.multiply(sat.get_position(utc, 0),1000)
	observerVelocityVector = getVelocityFromAngular(sat,lon,lat,alt,angularVelocity)
	angle1 = getAngleBetweenVectors(observerVelocityVector,distanceVector)
	velocity1 = getVectorMagnitude(observerVelocityVector)
	angle2 = getAngleBetweenVectors(satVelocityVector,distanceVector)
	velocity2 = getVectorMagnitude(satVelocityVector)
	relativeVelocity = velocity2*cos(radians(angle2))+velocity1*cos(radians(angle1))
	return relativeVelocity

def calcAngleToObserver(Re,ao,asat,el): #potato radius, observer altitude, satellite altitude, elevation from horizon
	cosElPN = cos(radians(el+90)) # cos(el+90deg)
	x = (Re+ao)*cosElPN+sqrt((Re+ao)**2*(cosElPN**2)+(Re+asat)**2) #distance between sat and observer
	cosGamma = ((Re+asat)**2+(Re+ao)**2-x**2)/(2*(Re+asat)*(Re+ao)) #calculate cosine of gamma (using cosine theorem) where gamma is the angle between the observer and the satellite from the center of the earth
	gamma = acos(cosGamma) # get the angle (in radians)
	return gamma 

def getDopplerShift(f,Vsx,Vo=0): #difference in frequencies (in KHz) for stationary observer
	#frequency in MHz, 1d velocity of satellite, 1d velocity of observer 
	c=299792458#speed of light in meters
	df=f*((c+Vo)/(c+Vsx)-1)
	return df*1e3

# print(getDopplerShift(436.5,getSatRelativeVelocity(sat, datetime.utcnow(),lon,lat,ao)),'KHz')

def main():
	el = 89.99999
	Re = getReAtLat(lat)
	h=450
	alt = 1.463
	d=Re+h
	gamma = radians(.5)
	c=sqrt(d**2*2-d**2*2*cos(gamma))
	cosElPN = cos(radians(el+90))
	x = h+5#(Re+alt)*(cosElPN)+sqrt((Re+h)**2*(cosElPN**2)+(Re+h)**2) 
	print(alt,x,c,degrees(gamma))
	phi = acos((h**2+x**2-c**2)/(2*h*x)) #rad
	arc = 2*pi*degrees(gamma)/360*d
	t=arc/8
	print(alt,x,c,arc,degrees(gamma),t)
	print(degrees(phi)/t)

main()

