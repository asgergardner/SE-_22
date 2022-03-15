import numpy as np
import matplotlib.pyplot as plt

def norm_pow(wl, plot):
    data1 = np.loadtxt("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Power/powerscan_220211_01.txt", skiprows=2)
    data2 = np.loadtxt("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Power/powerscan_220211_02.txt", skiprows=2)
    
    wls = data1[:,0]
    power = (data1[:,1] + data2[:,1])/2
    
    if plot:
        plt.figure()
        plt.plot(wls, power)
        plt.xlabel("Wavelength [nm]", fontsize=14)
        plt.ylabel("Power [mW]", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid()
        plt.locator_params(nbins=8)
        plt.show()
    
    idx = np.where(wls==wl)[0][0]
    pow0 = power[idx]
    
    
    return pow0*wl

# Just testing the function call
norm = norm_pow(575, False)