import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat

def spectrum_analysis(data_laser, data_nolaser, data_energy, offset, windowsA, windowsB, wl_range, E_column, plot):
    # Function for calculating cross section
    def cs(Na, Nb, Na0, Nb0, wl, E_pulse):
        return (Na - Na0*Nb/Nb0) / (Nb*E_pulse/(1/wl))
    
    # Function for calculating error using propagation
    def unc(Na, Nb, Na0, Nb0, wl, E_pulse, E_pulse_unc):
        return np.sqrt(Na*(1/(Nb*E_pulse*wl))**2 + Na0*(-1/(E_pulse*Nb0*wl))**2 \
            + Nb*(-Na/(E_pulse*wl)*1/Nb**2)**2 \
                + Nb0*(-Na0/(E_pulse*wl)*1/Nb0**2)**2 \
                    + E_pulse_unc**2*(-(Na-Nb*Na0/Nb0)/(Nb*wl*E_pulse**2))**2)

    # Importing 3 data files
    mcp_laser = np.loadtxt(data_laser, delimiter=",")
    mcp_nolaser = np.loadtxt(data_nolaser, delimiter=",")
    energy_data = np.loadtxt(data_energy)
    
    # Initialize time array of right length and relevant wavelength array
    lambda0 = wl_range[0]
    lambda1 = wl_range[1]
    ts = np.linspace(0,15000, len(mcp_nolaser))
    lambdas = np.linspace(lambda0, lambda1, len(mcp_laser))
    
    # Picking out energy and uncertainty from data file
    E_pulse = energy_data[:,E_column]
    E_pulse_unc = energy_data[:,E_column+1]  
    
    # Localize the index to place window A
    max_val = 0
    max_idx = 0
    for i in range(len(mcp_laser)):
        if max(mcp_laser[i]) > max_val:
            max_val = max(mcp_laser[i])
            max_idx = np.argmax(mcp_laser[i])
    #print("Max index is "+ str(max_idx))
    max_idx = 3654
    
    if plot: # Plotting background afo time
        plt.figure()
        plt.title("Background")
        plt.xlabel("Time [mu s]")
        plt.ylabel("Counts")
        plt.plot(ts, mcp_nolaser)
        plt.show()

    # Calculating the cross section and error using the function above. Also plot all histograms
    css = np.zeros(len(mcp_laser))
    uncs = np.zeros(len(mcp_laser))
    init_index = max_idx + offset
    windowB_index = 700
    for i in range(len(mcp_laser)):
        if plot:
            plt.figure(figsize=(12,4))
            plt.title(r"$\lambda$ = " + str(lambdas[i]))
            plt.xlabel(r"Time [$\mu$s]", fontsize=18)
            plt.ylabel("Counts", fontsize=18)
            plt.plot(ts, mcp_laser[i])
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            # plt.vlines(ts[init_index], 0, max(mcp_laser[i]), colors="red", linewidth=3)
            # plt.vlines(ts[-1], 0, max(mcp_laser[i]), colors="red", linewidth=3)
            # plt.hlines(0, ts[init_index], ts[-1], colors="red", linewidth=3)
            # plt.hlines(max(mcp_laser[i]), ts[max_idx], ts[-1], colors="red", linewidth=3)
            # plt.vlines(ts[windowB_index], 0, max(mcp_laser[i]), color="green", linewidth=3)
            # plt.vlines(ts[max_idx-200], 0, max(mcp_laser[i]), color="green", linewidth=3)
            # plt.hlines(0, ts[windowB_index], ts[max_idx-200], color="green", linewidth=3)
            # plt.hlines(max(mcp_laser[i]), ts[windowB_index], ts[max_idx-200], color="green", linewidth=3)
            plt.show()
        
        
        Na = sum(mcp_laser[i][windowsA[0]:windowsA[1]])
        Nb = sum(mcp_laser[i][windowsB[0]:windowsB[1]])
        Na0 = sum(mcp_nolaser[windowsA[0]:windowsA[1]])
        Nb0 = sum(mcp_nolaser[windowsB[0]:windowsB[1]])
        wl = lambdas[i]

        css[i] = cs(Na, Nb, Na0, Nb0, wl, E_pulse[i])
        uncs[i] = unc(Na, Nb, Na0, Nb0, wl, E_pulse[i], E_pulse_unc[i])

    # Plotting the cross section afo wavelength
    if plot:
        fig = plt.figure()
        plt.errorbar(lambdas, css, uncs)
        plt.grid()
        plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
        plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    else:
        fig = None
    
    return lambdas, css, uncs, fig

# cross1 = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_Laser_410-700_run001_15-02-22.txt", "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_NoLaser_410-700_run001_15-02-22.txt", False)
# cross2 = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/SED_Laser_410-700_run001_15-02-22.txt", "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/SED_NoLaser_410-700_run001_15-02-22.txt", False)
lambdas1_mcp, css1_mcp, uncs1_mcp, fig1_mcp = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_Laser_440_600_run012_15-02-22.txt", \
                           "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_NoLaser_440_600_run012_15-02-22.txt", \
                               "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_440-600.txt",
                               100, [3700, 12010], [1000, 3000], [440, 600], 11, True)
# lambdas1_sed, css1_sed, uncs1_sed, fig1_sed = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_Laser_440_600_run012_15-02-22.txt", \
#                                "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_NoLaser_440_600_run012_15-02-22.txt", \
#                                    "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_440-600.txt", 
#                                    100, [440, 600], 11, False)

lambdas2_mcp, css2_mcp, uncs2_mcp, fig2_mcp = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_Laser_404-450_run001_18-02-22.txt", \
                            "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_NoLaser_404-450_run001_18-02-22.txt", \
                                "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_404-450.txt",
                                100, [5555, 6510], [1050, 5000], [404, 450], 9, False)
# lambdas2_sed, css2_sed, uncs2_sed, fig2_sed = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_Laser_404-450_run001_18-02-22.txt", \
#                                 "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_NoLaser_404-450_run001_18-02-22.txt", \
#                                     "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_404-450.txt", 
#                                     100, [404, 450], 9, False)

lambdas3_mcp, css3_mcp, uncs3_mcp, fig3_mcp = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_Laser_390-404_run002_18-02-22.txt", \
                            "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_NoLaser_390-404_run002_18-02-22.txt", \
                                "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_390-404.txt",
                                100, [5555, 6510], [1050, 5000], [390, 404], 9, False)
# lambdas3_sed, css3_sed, uncs3_sed, fig3_sed = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_Laser_390-404_run002_18-02-22.txt", \
#                                 "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_NoLaser_390-404_run002_18-02-22.txt", \
#                                     "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_390-404.txt", 
#                                     100, [390, 404], 9, False)
    
lambdas4_mcp, css4_mcp, uncs4_mcp, fig4_mcp = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_Laser_352-392_run003_18-02-22.txt", \
                            "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_NoLaser_352-392_run003_18-02-22.txt", \
                                "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_352-392.txt",
                                100, [5555, 6510], [1050, 5000], [352, 392], 9, False)
# lambdas4_sed, css4_sed, uncs4_sed, fig4_sed = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_Laser_352-392_run003_18-02-22.txt", \
#                                 "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_NoLaser_352-392_run003_18-02-22.txt", \
#                                     "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_352-392.txt", 
#                                     100, [352, 392], 9, False)
        
lambdas5_mcp, css5_mcp, uncs5_mcp, fig5_mcp = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_Laser_300-360_run004_18-02-22.txt", \
                            "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_NoLaser_300-360_run004_18-02-22.txt", \
                                "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data_300-360.txt",
                                100, [5555, 6510], [1050, 5000], [300, 360], 9, False)

plt.figure(figsize=(12,6))
plt.errorbar(lambdas1_mcp, css1_mcp, uncs1_mcp, marker=".", markersize=10, capsize=3)
#plt.errorbar(lambdas1_sed, css1_sed, uncs1_sed, marker=".", markersize=10, capsize=3)
plt.grid()
plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.rc('font', size=14)
plt.locator_params(nbins=8)
plt.legend(["MCP-signal","SED-signal"], fontsize=12)
plt.show()

plt.figure(figsize=(12,6))
plt.errorbar(lambdas2_mcp, css2_mcp, uncs2_mcp, marker=".", markersize=10, capsize=3)
#plt.errorbar(lambdas2_sed, css2_sed, uncs2_sed, marker=".", markersize=10, capsize=3)
plt.grid()
plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.rc('font', size=14)
plt.locator_params(nbins=8)
plt.legend(["MCP-signal","SED-signal"], fontsize=12)
plt.show()

plt.figure(figsize=(12,6))
plt.errorbar(lambdas3_mcp, css3_mcp, uncs3_mcp, marker=".", markersize=10, capsize=3)
#plt.errorbar(lambdas3_sed, css3_sed, uncs3_sed, marker=".", markersize=10, capsize=3)
plt.grid()
plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.rc('font', size=14)
plt.locator_params(nbins=8)
plt.legend(["MCP-signal","SED-signal"], fontsize=12)
plt.show()

plt.figure(figsize=(12,6))
plt.errorbar(lambdas4_mcp, css4_mcp, uncs4_mcp, marker=".", markersize=10, capsize=3)
#plt.errorbar(lambdas4_sed, css4_sed, uncs4_sed, marker=".", markersize=10, capsize=3)
plt.grid()
plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.rc('font', size=14)
plt.locator_params(nbins=8)
plt.legend(["MCP-signal","SED-signal"], fontsize=12)
plt.show()

plt.figure(figsize=(12,6))
plt.errorbar(lambdas5_mcp, css5_mcp, uncs5_mcp, marker=".", markersize=10, capsize=3)
plt.grid()
plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.rc('font', size=14)
plt.locator_params(nbins=8)
plt.legend(["MCP-signal"], fontsize=12)
plt.show()

lambdas_mcp = np.concatenate([lambdas5_mcp, lambdas4_mcp, lambdas3_mcp, lambdas2_mcp, lambdas1_mcp])
css_mcp = np.concatenate([css5_mcp, css4_mcp, css3_mcp, css2_mcp, css1_mcp])
uncs_mcp = np.concatenate([uncs5_mcp, uncs4_mcp, uncs3_mcp, uncs2_mcp, uncs1_mcp])

css2_mcp = np.delete(css2_mcp, [0, 1, 19, 20, 21, 22, 23])
lambdas2_mcp = np.delete(lambdas2_mcp, [0, 1, 19, 20, 21, 22, 23])
uncs2_mcp = np.delete(uncs2_mcp, [0, 1, 19, 20, 21, 22, 23])

css4_mcp = np.delete(css4_mcp, [10])
lambdas4_mcp = np.delete(lambdas4_mcp, [10])
uncs4_mcp = np.delete(uncs4_mcp, [10])

css5_mcp = np.delete(css5_mcp, [13, 14, 15])
lambdas5_mcp = np.delete(lambdas5_mcp, [13, 14, 15])
uncs5_mcp = np.delete(uncs5_mcp, [13, 14, 15])

#lambdas_sed = np.concatenate([lambdas4_sed, lambdas3_sed, lambdas2_sed, lambdas1_sed])
#css_sed = np.concatenate([css4_sed/25, css3_sed/25, css2_sed/25, css1_sed])
#uncs_sed = np.concatenate([uncs4_sed/25, uncs3_sed/25, uncs2_sed/25, uncs1_sed])

plt.figure(figsize=(12,4))
#plt.errorbar(lambdas_mcp, css_mcp, uncs_mcp, marker=".", markersize=10, capsize=3)
#plt.errorbar(lambdas_sed, css_sed, uncs_sed, marker=".", markersize=10, capsize=3)
plt.errorbar(lambdas1_mcp, css1_mcp, uncs1_mcp, marker=".", markersize=10, capsize=3)
plt.errorbar(lambdas2_mcp, css2_mcp*5, uncs2_mcp, marker=".", markersize=10, capsize=3)
plt.errorbar(lambdas3_mcp, css3_mcp, uncs3_mcp, marker=".", markersize=10, capsize=3)
plt.errorbar(lambdas4_mcp, css4_mcp, uncs4_mcp, marker=".", markersize=10, capsize=3)
plt.errorbar(lambdas5_mcp, css5_mcp, uncs5_mcp, marker=".", markersize=10, capsize=3)
plt.grid()
plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.rc('font', size=14)
plt.locator_params(nbins=8)
plt.legend(["Sweep 1", "Sweep 2", "Sweep 3", "Sweep 4", "Sweep 5"], fontsize=12)
plt.show()

# plt.figure(figsize=(12,6))
# #plt.errorbar(lambdas_mcp, css_mcp, uncs_mcp, marker=".", markersize=10, capsize=3)
# #plt.errorbar(lambdas_sed, css_sed, uncs_sed, marker=".", markersize=10, capsize=3, color="orange")
# plt.grid()
# plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
# plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
# plt.rc('font', size=14)
# plt.locator_params(nbins=8)
# plt.show()