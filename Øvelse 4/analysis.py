import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
from load import do_load

def fitfunc(x, a, b, c, d):
    return a*(b**2/((x - c)**2 + b**2)) + d

Es, degs, data = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 4/Data/Au111.txt")

p0 = np.array([1000, 0.1, 13.3, 300])


E_kin = np.zeros(len(data))
for i in range(len(data)):
    if -4.5 < degs[i] and degs[i] < 4.5: 
        popt, pcov = curve_fit(fitfunc, Es, data[i], p0=p0)
        Es2 = np.linspace(Es[0],Es[-1], 1000)
        fit = fitfunc(Es2, popt[0], popt[1], popt[2], popt[3])
        
        E_kin[i] = popt[2]
        
        plt.figure()
        plt.title("Angle is " + str(degs[i]))
        plt.xlabel("Kinetic energy")
        plt.ylabel("Intensity")
        plt.plot(Es, data[i], "k")
        plt.plot(Es2, fit, "r")
        plt.show()
        
#%%
plt.figure()
plt.plot(degs, E_kin, ".")
plt.xlim(-5.4,5.4)
plt.ylim(13.1, 13.6)
plt.xlabel("Degress")
plt.ylabel("Kinetic energy")
plt.show()

E_F = 13.593
degs_deg = [math.radians(degs[i]) for i in range(len(degs))]
k = 0.512*np.sqrt(E_kin)*np.sin(degs_deg)
E_bin = E_kin - E_F

plt.figure()
plt.plot(degs, E_bin, ".")
plt.xlim(-5.4,5.4)
plt.ylim(-0.6, 0)
plt.xlabel("Degress")
plt.ylabel("Binding energy")
plt.show()

def fitfunc2(x, a, b):
    return a*x**2 + b

k_new = np.delete(k, np.where(E_bin< -5)[0])
E_bin_new = np.delete(E_bin, np.where(E_bin< -5)[0])

p0 = np.array([1, -1])
popt, pcov = curve_fit(fitfunc2, k_new, E_bin_new, p0=p0)

ks = np.linspace(-0.15, 0.15, 1000)
fit2 = fitfunc2(ks, popt[0], popt[1])


plt.figure()
plt.plot(k_new, E_bin_new, "k.")
plt.plot(ks, fit2, "r-")
#plt.xlim(-5.4,5.4)
#plt.ylim(-0.5, 0)
plt.xlabel("Wave vector $k_{||}$ [Å$^{-1}$]")
plt.ylabel("Binding energy $E_{bin}$ [eV]")
plt.show()


