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
    

#%% Making the cool plot
E_F = 13.593
fg = plt.figure()
for i in range(len(data)):
    if i%5 == 0:
        if -4.5 < degs[i] and degs[i] < 4.5: 
            toPlot = data[i]/np.max(data[i]) + i/30
            plt.plot(Es, toPlot, "k")
plt.vlines(E_F, 5, 14, "r", linestyles="dashed")
plt.ylim(6,13.2)
plt.xlim(12.6, 14.4)
plt.yticks(color='w')
plt.tick_params(left = False)
plt.text(E_F-0.03,13.5,r"$E_F$", fontsize=15, color="red")
plt.xlabel("Kinetic energy [eV]")
plt.ylabel("Photoemission intensity [arb. units]")
plt.text(14.03,6.3,r"$-4.5$", fontsize=15, color="black")
plt.text(14.03,6.3+6.0,r"$+4.5$", fontsize=15, color="black")
plt.text(14.20,9.3,r"$\theta$ [$^o$]", fontsize=15, color="black")
plt.arrow(14.15, 6.9, 0, 4.7, width=0.01, color="black", head_length=0.4, head_width=0.07)
plt.show()

#%% (SI units)
hbar = 1.055e-34
m = 9.109383632e-31
eV_2_J = 1.602e-19
invM_2_invÅ = 1e-10
degs_deg = [math.radians(degs[i]) for i in range(len(degs))]

E_F_SI = 13.593*eV_2_J

E_kin_SI = E_kin*eV_2_J
E_bin_SI = E_kin_SI - E_F_SI
k_SI = np.sqrt(2*m/hbar**2)*np.sqrt(E_kin_SI)*np.sin(degs_deg)

k_new_SI = np.delete(k_SI, np.where(E_bin_SI< -0.5e-18)[0])
E_bin_new_SI = np.delete(E_bin_SI, np.where(E_bin_SI< -0.5e-18)[0])

def fitfunc2(x, a, b):
    return a*x**2 + b

p0 = np.array([1, -7e-20])
popt, pcov = curve_fit(fitfunc2, k_new_SI, E_bin_new_SI, p0=p0)

ks = np.linspace(-0.15/invM_2_invÅ, 0.15/invM_2_invÅ, 1000)
fit2 = fitfunc2(ks, popt[0], popt[1])

plt.figure()
plt.plot(k_new_SI, E_bin_new_SI, "k.")
plt.plot(ks, fit2, "r-")
plt.xlabel("Wave vector $k_{||}$ [m$^{-1}$]")
plt.ylabel("Binding energy $E_{bin}$ [J]")
plt.show()

plt.figure()
plt.plot(k_new_SI*invM_2_invÅ, E_bin_new_SI/eV_2_J, "k.")
plt.xlabel("Wave vector $k_{||}$ [m$^{-1}$]")
plt.ylabel("Binding energy $E_{bin}$ [J]")
plt.show()

m_eff = hbar**2/(2*popt[0])
print("Effective mass is: " + str(m_eff/m) + " electron masses")

#%% Temporary plots and fit (units off)
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


