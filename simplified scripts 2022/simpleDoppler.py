from math import *
import turtle
import numpy as np
r1 = 6378.14e3 #earth equatorial radius
r2 = 6356.75e3 #earth polar radius
Re = (r1+r2)/2 #earth mean radius in m
G=6.674e-11 #gravitational constant
Me=5.972e24#earth mass in kg

def Rotate(v, x,y,z):#rotate a vector using matrices to transform along x y and z axes
    x,y,z=radians(x),radians(y), radians(z)
    rx = np.array([[1,0,0],[0, cos(x), -sin(x)],[0,sin(x), cos(x)]])
    ry = np.array([[cos(y),0,sin(y)],[0,1,0],[-sin(y),0,cos(y)]])
    rz = np.array([[cos(z),-sin(z),0],[sin(z),cos(z),0],[0,0,1]])
    return np.matmul(np.matmul(np.matmul(rx,ry),rz),v)

def Position(lon,lat, alt=0, incl=0):#define a position on an circle orbit given longtitude, latitude and altitude above Re on a sphere, and orbit inclination, regarding the X axis 
    observerCircleRadius = (Re+alt)*sin(radians(90-lat))
    observerDistanceFromCenter = (Re+alt)*cos(radians(90-lat))
    return np.transpose(Rotate(np.array([[observerCircleRadius], [0], [observerDistanceFromCenter]]),incl,0,lon))

def elevationAngle(posObs, posSat):#get the elevation angle between observer and satellite positions 
    return degrees(asin(round(np.linalg.norm(np.cross(posSat-posObs,posSat))/np.linalg.norm(posSat)/np.linalg.norm(posObs),6)))

def velocityAngleCos(velocity, direction):#get the cosine of the angle between a velocity vector and another direction (two directions)
    return np.dot(velocity[0],direction[0])/np.linalg.norm(velocity)/np.linalg.norm(direction)

def speed(alt):#get orbital speed at an altitude
    return sqrt(Me*G/(Re+alt))

def velocity(lon,alt,incl):#get velocity vector, regarding a body position at an orbit (always tangent to orbit)
    return np.transpose(Rotate(np.array([[0],[speed(alt)], [0]]),incl,0,lon))

def shift(freq,speed): #get Doppler frequency shift
    return speed/3e8*freq

#the code below was used to generate values to plot the frequency shift against the elevation angle of a satellite passing over a ground station at the equator
"""
observer = Position(0,0,100)
sat = Position(0,0,600e3,0)

for i in range(-900,900):
    i/=10
    incl, alt=0, 100e3
    sat = Position(i,0,alt,incl)
    vel = velocity(i,alt,incl)
    #print(speed(alt)*(velocityAngleCos(vel,sat-observer))/1000)
    print(shift(440e6,speed(alt)*(velocityAngleCos(vel,sat-observer)))/1000,'\t\t\t',np.sign(i)*elevationAngle(observer,sat))
"""