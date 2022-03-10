import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def mass_analysis(data, data_nolaser, run, plot):
    data_raw = np.loadtxt(data, delimiter=",")
    data_nolaser = np.loadtxt(data_nolaser, delimiter=",")
    
    ts = np.linspace(0, 15000, len(data_nolaser)) # 15000 mu s
    
    if run == 1:
        ms = np.arange(130, 201)
    if run == 2:
        ms = np.arange(115, 259)
    
    data = data_raw - data_nolaser
    
    counts = np.zeros(len(data))
    for i in range(len(data)):
        if plot:
            plt.figure()
            plt.plot(ts, data[i])
            plt.title("Investigating mass of " + str(ms[i]))
            #plt.vlines(ts[5600], 0, 1000, "r")
            #plt.vlines(ts[5700], 0, 1000, "r")
            plt.figure()
        
        counts[i] = sum(data[i][5600:5700])
        
    uncs = np.sqrt(counts)
    fig = plt.figure()

    plt.errorbar(ms, counts, uncs, marker=".", markersize=10, capsize=3)
    plt.xlabel("Dumped mass [amu]")
    plt.ylabel("Counts")
    plt.grid()
    plt.show()
    
    return ms, counts, uncs, fig

m0 = 273

ms1, counts1, uncs1, fig1 = mass_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Daughter mass data - 17.2/MCP_Laser_130-200_run008_17-02-22.txt",
              "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Daughter mass data - 17.2/MCP_NoLaser_130-200_run008_17-02-22.txt", 
              1, False)

ms2, counts2, uncs2, fig2 = mass_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Daughter mass data - 17.2/MCP_Laser_115-258_run007_17-02-22.txt",
              "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Daughter mass data - 17.2/MCP_NoLaser_115-258_run007_17-02-22.txt", 
              2, False)

a = 1.00
b = 7.65
plt.figure(figsize=(12,6))
plt.errorbar(m0 - (ms1*a + b), counts1, uncs1, marker=".", markersize=10, capsize=3)
plt.errorbar(m0 - (ms2[85:-1]*a + b), counts2[85:-1], uncs2[85:-1], marker=".", markersize=10, capsize=3)
plt.xlabel("Daughter mass [amu]", fontsize=14)
plt.ylabel("Counts", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(["Sweep 1","Sweep 2"], fontsize=12)
plt.grid()
plt.show()

def fitfunc(x, a, b, c, d):
    return a*np.exp(-(x-b)**2/c**2) + d

ms = m0 - np.concatenate((ms1, ms2[85:-1]), axis = 0)
ms = np.flip(ms)
counts = np.concatenate((counts1, counts2[85:-1]), axis = 0)
counts = np.flip(counts)
uncs = np.concatenate((uncs1, uncs2[85:-1]), axis = 0)
uncs = np.flip(uncs)

q = [25, 42, 56, 68, 83, 99, 108]
p0 = [[100, 35, 5, 1],
      [100, 50, 5, 1],
      [100, 62, 5, 1],
      [50, 75, 5, 1],
      [50, 90, 5, 1],
      [400, 104, 1, 1]]

cen = np.zeros(len(q) - 1)
cen_unc = np.zeros(len(q) - 1)

for i in range(len(q) - 1):
    if i != 6:
        popt, pcov = curve_fit(fitfunc, ms[np.where(ms == q[i])[0][0] : np.where(ms == q[i+1])[0][0]], 
                       counts[np.where(ms == q[i])[0][0] : np.where(ms == q[i+1])[0][0]], 
                       p0=p0[i], sigma=uncs[np.where(ms == q[i])[0][0] : np.where(ms == q[i+1])[0][0]]+0.1, 
                       absolute_sigma=True, maxfev=10000)
    
    mss = np.linspace(q[i], q[i+1], 1000)
    plt.figure()
    if i != 6:
        plt.plot(mss, fitfunc(mss, popt[0], popt[1], popt[2], popt[3]), "r-")
    plt.errorbar(ms[np.where(ms == q[i])[0][0] : np.where(ms == q[i+1])[0][0]], 
                 counts[np.where(ms == q[i])[0][0] : np.where(ms == q[i+1])[0][0]], 
                 uncs[np.where(ms == q[i])[0][0] : np.where(ms == q[i+1])[0][0]])
    plt.show()
    
    cen[i] = popt[1]
    cen_unc[i] = np.sqrt(np.diag(pcov))[1]

plt.figure(figsize=(8,4))
plt.errorbar(m0 - (ms1*a + b), counts1, uncs1, marker=".", markersize=10, capsize=3)
plt.errorbar(m0 - (ms2[85:-1]*a + b), counts2[85:-1], uncs2[85:-1], marker=".", markersize=10, capsize=3)
plt.legend(["Sweep 1","Sweep 2"], fontsize=12)
for i in range(len(q)-1):
    plt.vlines(cen[i]*a - b, 0, max(counts2), linestyles="dashed", colors="red", linewidth=3)
plt.xlabel("Daughter mass [amu]", fontsize=14)
plt.ylabel("Counts", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid()
plt.show()
    
   
print("The daughter masses are:")
for i in range(len(q)-1):
    print(str(cen[i]-b) + " +- " + str(cen_unc[i]))