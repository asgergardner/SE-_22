from load import do_load
from power_analysis import norm_pow
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import integrate

def abs_analysis(plotfinal, plot):
    filenums = np.arange(7,49) # File numbers
    
    wls = np.zeros(len(filenums)) # Arrays to be filled
    signal = np.zeros(len(filenums))
    
    for i in range(len(filenums)):
        if filenums[i] < 10:
            str_end = "0" + str(filenums[i]) # Add extra 0 to filenumbers < 10
        else: str_end = str(filenums[i])
        
        wl, tab = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/FE/220308" + str_end + "_LUNA.dat")
        
        if plot:
            plt.figure()
            plt.plot(tab[:,0], tab[:,3])
            plt.xlabel("Wavelength [nm]", fontsize=14)
            plt.ylabel("Signal yield [arb. units]", fontsize=14)
            plt.title("Probe wavelength: " + str(wl))
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
            plt.rc('font', size=14)
            plt.grid()
            plt.locator_params(nbins=8)
            plt.show()
            
        f = interpolate.interp1d(tab[:,0], tab[:,3]) # Interpolate the data
        
        wl_new = np.linspace(min(tab[:,0]), max(tab[:,0]), 1000)
        interp = f(wl_new)
        s = integrate.trapz(interp) # Integrate the interpolant
    
        wls[i] = wl # Save probe wavelength in array
        signal[i] = s/norm_pow(round(wl), False) # Normalize the signal with flux and save in array
        
    
    pairs = zip(wls, signal) # Zip values together
    res = sorted(pairs) # Sort according to wavelength
    
    wl_res = [x[0] for x in res] # Pick out the zipped values
    signal_res = [x[1] for x in res] # Pick out the zipped values
    
    if plotfinal:
        plt.figure(figsize=(8,4))
        plt.errorbar(wl_res, np.array(signal_res)/0.003903012791611044, np.array(np.sqrt(np.absolute(signal_res)))/0.003903012791611044, marker=".", color="blue", markersize=10, capsize=4)
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
        plt.show()
    
    return np.array(wl_res), np.array(signal_res), np.array(np.sqrt(np.absolute(signal_res)))
    
wl, sig, uncs = abs_analysis(True, False)