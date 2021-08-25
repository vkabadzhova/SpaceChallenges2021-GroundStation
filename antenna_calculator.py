from math import *
c=3e8
G=1.66
fmin,fmax=float(input('Minimum  frequency (MHz): ')), float(input('Maximum frequency (MHz): '))
N=int(input('Number of directors: '))
f=(fmax+fmin)/2
wavelength=c/f/100 #in cm
R=round(105/100*wavelength/2)/100
A=round(wavelength/2)/100
D=round(.9*wavelength/2)/100
RA=round(wavelength/4)/100
AD=round(.28*wavelength)/100
DD=round(wavelength/3)/100
L2=round(wavelength/2)/100
B=round(RA+AD+DD*(N-1)+10)/100
Gain=round(100*G*(N+2))/100
print(f'Optimized for frequency of {f}MHz\nLength of Reflector: {R}cm\nDriven element length: {A} cm\nDirector length: {D} cm\nSpacing between Reflector and Driven element: {RA} cm\nSpacing between Driven element and Director: {AD} cm\nSpacing between Directors: {DD} cm\nApproximate gain: {Gain} dBi\nLength of Boom: {B} m')
