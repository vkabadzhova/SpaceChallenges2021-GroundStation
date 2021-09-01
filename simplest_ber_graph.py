# Import the necessary packages and modules
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from math import *
from scipy import special
# Prepare the data
def qfunc(x):
    return 1/2*special.erfc(x/np.sqrt(2))
def berfunc(x):
    return qfunc(10**(np.sqrt(2*x)/10))

x = np.linspace(-3, 35)
y=berfunc(x)
plt.plot(x, y, '--bo',label='Error function', color='red')
plt.yscale('log')
plt.ylim([10e-8, 10e-1])
plt.xlim([1,35])
plt.xlabel("Eb/No")
plt.ylabel("BER")
plt.title("Simplest modulation scheme")
plt.stem(x,y,'--',  orientation='vertical')    
plt.hlines(y,-10,36)   
plt.vlines(x,0,10e100)   

# Add a legend
plt.legend()
# Show the plot
plt.show()