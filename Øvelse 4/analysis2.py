import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
from load import do_load

def fitfunc(x, a, b, c, d):
    return a*(b**2/((x - c)**2 + b**2)) + d

Es, degs, data = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 4/Data/Au111.txt")

p0 = np.array([1000, 0.1, 13.3, 300])

E_F = 13.593

E_kin = np.zeros(len(data))
E_kin_uncs = np.zeros(len(data))
for i in range(len(data)):
    if -5.5 < degs[i] and degs[i] < 5.5: 
        uncs = np.sqrt(data[i])
        
        Es_toFit = np.delete(Es, np.where(Es > E_F))
        toFit = np.delete(data[i], np.where(Es > E_F))
        uncs_toFit = np.delete(uncs, np.where(Es > E_F))

#        popt, pcov = curve_fit(fitfunc, Es, data[i], p0=p0, sigma=uncs, absolute_sigma=True)
        popt, pcov = curve_fit(fitfunc, Es_toFit, toFit, p0=p0, sigma=uncs_toFit, absolute_sigma=True)
        Es2 = np.linspace(Es[0],Es[-1], 1000)
        fit = fitfunc(Es2, popt[0], popt[1], popt[2], popt[3])
        
        E_kin[i] = popt[2]
        E_kin_uncs[i] = np.sqrt(pcov[2,2])
        
        plt.figure()
        plt.title("Angle is " + str(degs[i]))
        plt.xlabel("Kinetic energy")
        plt.ylabel("Intensity")
        plt.errorbar(Es, data[i], yerr=uncs, color="black")
        plt.plot(Es2, fit, "r")
        plt.show()
    

#%% Making the cool plot
E_F = 13.593
fg = plt.figure(figsize=(12,7))
for i in range(len(data)):
    if i%5 == 0:
        if -5.5 < degs[i] and degs[i] < 5.5: 
            toPlot = data[i]/np.max(data[i]) + i/30 + 0.25
            plt.plot(Es, toPlot, "k")
plt.vlines(E_F, 5, 15, "r", linestyles="dashed")
plt.ylim(5.5,14.5)
plt.xlim(12.6, 14.20)
plt.yticks(color='w')
plt.tick_params(left = False)
plt.text(E_F-0.03,14.7,r"$E_F$", fontsize=18, color="red")
plt.xlabel("Kinetic energy [eV]", fontsize=16)
plt.ylabel("Photoemission intensity [arb. units]", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.text(13.98,5.9,r"$-5.5$", fontsize=18, color="black")
plt.text(13.98,5.9+7.0,r"$+5.5$", fontsize=18, color="black")
plt.text(14.07,9.3,r"$\theta$ [$^o$]", fontsize=18, color="black")
plt.arrow(14.05, 6.5, 0, 5.7, width=0.01, color="black", head_length=0.4, head_width=0.07)
#plt.savefig("slice.eps", format="eps")
plt.show()

#%% (SI units)
hbar = 1.055e-34
m = 9.109383632e-31
eV_2_J = 1.602e-19
invM_2_invÅ = 1e-10
degs_deg = [math.radians(degs[i]) for i in range(len(degs))]

E_F_SI = 13.593*eV_2_J
E_F_unc_SI = 8e-5*eV_2_J

E_kin_SI = E_kin*eV_2_J
E_kin_uncs_SI = E_kin_uncs*eV_2_J
E_bin_SI = E_kin_SI - E_F_SI
k_SI = np.sqrt(2*m/hbar**2)*np.sqrt(E_kin_SI)*np.sin(degs_deg)

k_new_SI = np.delete(k_SI, np.where(E_bin_SI< -0.5e-18)[0])
E_bin_new_SI = np.delete(E_bin_SI, np.where(E_bin_SI< -0.5e-18)[0])
E_kin_uncs_new_SI = np.delete(E_kin_uncs_SI, np.where(E_bin_SI< -0.5e-18)[0])
E_kin_uncs_new_SI2 = np.sqrt(E_kin_uncs_new_SI**2 + E_F_unc_SI**2)


def fitfunc2(x, a, b):
    return hbar**2*x**2/(2*a) + b

p0 = np.array([0.28*m, -7e-20])
popt, pcov = curve_fit(fitfunc2, k_new_SI, E_bin_new_SI, p0=p0, sigma=E_kin_uncs_new_SI2, absolute_sigma=True)

ks = np.linspace(-0.18/invM_2_invÅ, 0.18/invM_2_invÅ, 1000)
fit2 = fitfunc2(ks, popt[0], popt[1])

plt.figure(figsize=(12,7))
plt.errorbar(k_new_SI, E_bin_new_SI, yerr=E_kin_uncs_new_SI, color="black", marker=".", markersize=10, capsize=4, label="Data points", barsabove=True)
plt.plot(ks, fit2, "r-", linewidth=3, label="Dispersion fit")
plt.grid()
plt.legend(fontsize=16, loc="upper right")
plt.xlabel("Wave vector $k_{||}$ [m$^{-1}$]", fontsize=16)
plt.ylabel("Binding energy $E_{bin}$ [J]", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()

m_eff = popt[0]
print("Effective mass is: (" + str(m_eff/m) + " \pm " + str(np.sqrt(pcov[0,0])/m) + ") electron masses")

#%% (Natural units, just for plot)
def fitfunc2(x, a, b):
    return a*x**2 + b

E_F = 13.593
E_F_unc = 8e-5
degs_deg = [math.radians(degs[i]) for i in range(len(degs))]
k = 0.512*np.sqrt(E_kin)*np.sin(degs_deg)
E_bin = E_kin - E_F

k_new = np.delete(k, np.where(E_bin< -5)[0])
E_bin_new = np.delete(E_bin, np.where(E_bin< -5)[0])
E_kin_uncs_new = np.delete(E_kin_uncs, np.where(E_bin< -5)[0])
E_kin_uncs_new2 = np.sqrt(E_kin_uncs_new**2 + E_F_unc**2)


p0 = np.array([1, -1])
popt, pcov = curve_fit(fitfunc2, k_new, E_bin_new, p0=p0, sigma=E_kin_uncs_new2, absolute_sigma=True)

ks = np.linspace(-0.18, 0.18, 1000)
fit2 = fitfunc2(ks, popt[0], popt[1])

idx = np.where(E_bin_new == min(E_bin_new))[0]

plt.figure(figsize=(12,7))
plt.errorbar(k_new, E_bin_new, yerr=E_kin_uncs_new2*5, color="black", marker=".", markersize=10, capsize=4, label="Data points", barsabove=True)
plt.plot(ks, fit2, "r-", linewidth=3, label="Dispersion fit")
plt.vlines(k_new[idx], -0.5, 0, color="blue", linestyles="dashed")
plt.grid()
plt.legend(fontsize=16, loc="lower right")
plt.xlabel("Wave vector $k_{||}$ [Å$^{-1}$]", fontsize=16)
plt.ylabel("Binding energy $E_{bin}$ [eV]", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig("dispersion_data.eps", format="eps")
plt.show()