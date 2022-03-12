from math import *

def dB(a):
    return 10*log10(a)

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
def BER(SNR):
    return erfc(sqrt(10**(SNR/10)))/2 #QPSK

def PER():#packet eror rate from txt file or from given BER, only true for QPSK (2QPSK) modulation scheme
    return 1-e**(64*log(1-BER()))
def PER(BER):
    return 1-e**(64*log(1-BER))


#the code below was used to generate values for graphs (BER/SNR) and (BER/Receiver Gain)
""" 
def fastMath1():
    resolution=10
    #param['Ts']=dB(1500)
    calc={}
    for i in range(10*resolution,20*resolution+1):
        param['Gr']=i/resolution
        names=['SNR','BER','PER','Gr']
        calc[param['Gr']] = (SNR(),BER(),PER())
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