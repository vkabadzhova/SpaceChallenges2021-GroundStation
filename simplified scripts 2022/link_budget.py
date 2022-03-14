from math import *
from scipy import special

packetSize=64 #bits/symbols

def dB(a):
    return 10*log10(a)
def dBinv(a):#inverse function
    return 10**(a/10)

parameters = ['Gt','Pt','Gr','Ts','r','Freq','La','R']
param={}#all in dB

f=('kB=-228.5dB\n'+open('link_budget.txt').read()).split('\n')
for line in f: #reads static values from file and asks for missing values, then converts into decibel notation
    #use dB or dBm for units inside the txt file, otherwise do not write any unit
    if len(line.strip())<=0: break
    left, right = line.split('=')
    right=right.strip()
    right = input(left+': ') if len(right) <= 0 else right
    right = float(right.replace('dB','')) if right.endswith('dB') else (float(right.replace('dBm',''))-30) if right.endswith('dBm') else dB(float(right))
    param[left]=right

def Ls():#free space path loss
    return -2*(dB(3e8)-param['Freq']-dB(4*pi)-param['r'])
def SNR():#signal-to-noise-ratio or Eb/No
    return param['Gt']+param['Pt']+param['Gr']-param['Ts']-Ls()-param['La']-param['kB']-param['R']

def BER():#bit eror rate from txt file or from given SNR
    return erfc(sqrt(10**(SNR()/10)))/2 #QPSK
def BER2(SNR):
    return erfc(sqrt(10**(SNR/10)))/2 #QPSK

def PER():#packet eror rate from txt file or from given BER, only true for QPSK (2QPSK) modulation scheme
    return 1-e**(packetSize*log(1-BER()))
def PER2(BER):
    return 1-e**(packetSize*log(1-BER))


def BERinv(per):#inverse function
    return 1-(1-per)**(1/64)
def SNRinv(ber):#inverse function
    return 10*2*log10(special.erfcinv(2*ber))


def standardDeviation(values):
    avg=0
    for a in values:
        avg+=a
    avg/=len(values)
    meanQuadratic=0
    for a in values:
        meanQuadratic+=(a-avg)**2
    meanQuadratic=(meanQuadratic/len(values))**.5
    return meanQuadratic

#the code below was used to generate values for graphs (BER/SNR) and (BER/Receiver Gain)
######################################################################################
"""
def fastMath1():
    resolution=1
    #param['Ts']=dB(1500)
    pers=[99.33,94.35,77.915,59.05,50.5,48,42.225,44.57,45.725,45.2,40.965,39.55,43.35]
    calc={}
    for i in range(10*resolution,22*resolution+1):
        param['Gr']=i/resolution
        names=['SNR','BER','PER', 'BERinv', 'SNRinv','Gr']
        calc[param['Gr']] = (SNR(),BER(),PER(),BERinv(pers[i-10]/100),SNRinv(BERinv(pers[i-10]/100)))
        #print(SNR(),'\t', BER(),'\t\t\t',PER())

    print(names[-1])
    for i in sorted(calc.keys()):
        print(i)
    print('\n')
    for i in range(len(list(calc.values())[0])):
        print(names[i])
        for j in sorted(calc.keys()):
            print(calc[j][i])
        print('\n')

def fastMath2():
    resolution=5
    #param['Ts']=dB(1500)
    calc={}
    for i in range(1*resolution,40*resolution+1):
        names=['BER','PER','SNR']
        calc[i/resolution] = (BER(i/resolution),PER(BER(i/resolution)))
        #print(SNR(),'\t', BER(),'\t\t\t',PER())

    print(names[-1])
    for i in sorted(calc.keys()):
        print(i)
    print('\n')
    for i in range(len(list(calc.values())[0])):
        print(names[i])
        for j in sorted(calc.keys()):
            print(calc[j][i])
        print('\n')

"""