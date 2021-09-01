from math import log10, pi

""" 
QMR - KWT 

G_t -> Gain of UHF transciever
P_t -> Power of transmission
h_max -> Max altitude from GS
f -> Frequency of transmission
G_r -> Gain of ground station antenna
T_s -> System temperature
R -> Transmission rate
La -> Atmospheric losses
Lp -> Polarization losses
Ls -> Free space losses
Kb -> Botlzman constant
C -> Speed of light

"""
c = 299792458 # [m/s]

G_t = 0
P_t = -3.5  # [dBW]
h_max = 2.5e6 # [m]
f   = 436.5e6 # [MHz]
G_r = 16.6    # [dBi]
T_s = 320   # [K]
R   = 9600  # [bps]
La = 1  # [dB]
Lp = 3  # [dB]
Ls = 20 * log10(4 * pi * h_max * f / c) #[dB]
Kb = 228.5 # [dB]

def getEbNo():
    Gr_Ts = G_r - 10 * log10(T_s)
    return G_t + P_t + Gr_Ts - La - Ls - Lp + Kb - 10 * log10(R)

def main():
    Eb_No = getEbNo()
    print("Energy per bit per noise ratio (Eb/No): ", Eb_No)

if __name__ == "__main__":
    main()