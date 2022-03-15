from load import do_load
import matplotlib.pyplot as plt
import numpy as np

def flo_analysis(plot):
    wl05, tab05 = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Fluorescence/22030803_LUNA.dat")
    wl15_1, tab15_1 = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Fluorescence/22030803_LUNA.dat")
    wl15_2, tab15_2 = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Fluorescence/22030803_LUNA.dat")
    wl15_3, tab15_3 = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Fluorescence/22030803_LUNA.dat")
    
    
    tab15 = tab15_1[:,3] + tab15_2[:,3] + tab15_3[:,3]
    
    if plot:
        plt.figure(figsize=(8,4))
        plt.errorbar(tab05[:,0], tab05[:,3], np.sqrt(np.absolute(tab05[:,3])), marker=".", color="red", markersize=10, capsize=4)
        plt.errorbar(tab05[:,0], tab15, np.sqrt(np.absolute(tab15)), marker=".", color="green", markersize=10, capsize=4)
        plt.xlabel("Wavelength [nm]", fontsize=14)
        plt.ylabel("Yield [arb. units]", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.rc('font', size=14)
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.grid()
        plt.locator_params(nbins=8)
        plt.tick_params(bottom=True, top=True, right=True, left=True,
                        direction="in", length=7, width=1.2)
        plt.legend(["OD = 0.5","OD = 1.5"], fontsize=14)
        plt.show()
        
    return np.array(tab05[:,0]), np.array((tab05[:,3]+tab15)/2), np.array(np.sqrt(np.absolute((tab05[:,3]+tab15)/2)))

wl, sig, unc = flo_analysis(True)
