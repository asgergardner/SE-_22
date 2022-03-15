import numpy as np
import matplotlib.pyplot as plt

def norm_pow(wl, plot):
    data1 = np.loadtxt("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Power/powerscan_220211_01.txt", skiprows=2)
    data2 = np.loadtxt("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Power/powerscan_220211_02.txt", skiprows=2)
    
    wls = data1[:,0]
    power = (data1[:,1] + data2[:,1])/2
    
    if plot:
        plt.figure(figsize=(8,4))
        plt.plot(wls, power, color="black")
        plt.xlabel("Wavelength [nm]", fontsize=14)
        plt.ylabel("Power [mW]", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid()
        plt.locator_params(nbins=8)
        plt.tick_params(bottom=True, top=True, right=True, left=True,
                        direction="in", length=7, width=1.2)
        plt.show()

    
    if wl%1 == 0:
        idx = np.where(wls==wl)[0][0]
        pow0 = power[idx]
        
    else:
        wl0 = np.floor(wl)
        wl1 = np.ceil(wl)
        idx0 = np.where(wls==wl0)[0][0]
        idx1 = np.where(wls==wl1)[0][0]
        pow0 = (power[idx0] + power[idx1])/2 # average
    
    
    return pow0*wl

# Just testing the function call
norm = norm_pow(575, True)