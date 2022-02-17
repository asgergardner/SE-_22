import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat

def spectrum_analysis(data_laser, data_nolaser, data_energy, plot):
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
    ts = np.linspace(0,15000, len(mcp_nolaser))
    lambdas = np.linspace(440, 600, len(mcp_laser))
    
    # Picking out energy and uncertainty from data file
    E_pulse = energy_data[:,11]
    E_pulse_unc = energy_data[:,12]  
    
    # Localize the index to place window A
    max_val = 0
    max_idx = 0
    for i in range(len(mcp_laser)):
        if max(mcp_laser[i]) > max_val:
            max_val = max(mcp_laser[i])
            max_idx = np.argmax(mcp_laser[i])
    
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
    offset = 10 # Displacing index for begginning window A
    init_index = max_idx + offset
    windowB_index = 700
    for i in range(len(mcp_laser)):
        if plot:
            plt.figure()
            plt.title(r"$\lambda$ = " + str(lambdas[i]))
            plt.xlabel("Time [mu s]")
            plt.ylabel("Counts")
            plt.plot(ts, mcp_laser[i])
            plt.vlines(ts[init_index], 0, max(mcp_laser[i]), colors="red", linewidth=3)
            plt.vlines(ts[-1], 0, max(mcp_laser[i]), colors="red", linewidth=3)
            plt.hlines(0, ts[init_index], ts[-1], colors="red", linewidth=3)
            plt.hlines(max(mcp_laser[i]), ts[max_idx], ts[-1], colors="red", linewidth=3)
            plt.vlines(ts[windowB_index], 0, max(mcp_laser[i]), color="green", linewidth=3)
            plt.vlines(ts[max_idx-200], 0, max(mcp_laser[i]), color="green", linewidth=3)
            plt.hlines(0, ts[windowB_index], ts[max_idx-200], color="green", linewidth=3)
            plt.hlines(max(mcp_laser[i]), ts[windowB_index], ts[max_idx-200], color="green", linewidth=3)
            plt.show()
        
        
        Na = sum(mcp_laser[i][(init_index):-1])
        Nb = sum(mcp_laser[i][windowB_index:(init_index-200)])
        Na0 = sum(mcp_nolaser[(init_index):-1])
        Nb0 = sum(mcp_nolaser[windowB_index:(init_index-200)])
        wl = lambdas[i]
        
        css[i] = cs(Na, Nb, Na0, Nb0, wl, E_pulse[i])
        uncs[i] = unc(Na, Nb, Na0, Nb0, wl, E_pulse[i], E_pulse_unc[i])

    # Plotting the cross section afo wavelength
    fig = plt.figure()
    plt.errorbar(lambdas, css, uncs)
    plt.grid()
    plt.xlabel(r"Wavelength $\lambda$ [nm]", fontsize=14)
    plt.ylabel(r"Cross section $\sigma$ [arb. units]", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()
    
    return lambdas, css, uncs, fig

# cross1 = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_Laser_410-700_run001_15-02-22.txt", "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_NoLaser_410-700_run001_15-02-22.txt", False)
# cross2 = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/SED_Laser_410-700_run001_15-02-22.txt", "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/SED_NoLaser_410-700_run001_15-02-22.txt", False)
lambdas1, css1, uncs1, fig1 = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_Laser_440_600_run012_15-02-22.txt", \
                           "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/MCP_NoLaser_440_600_run012_15-02-22.txt", \
                               "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data.txt", False)
lambdas2, css2, uncs2, fig2 = spectrum_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_Laser_440_600_run012_15-02-22.txt", \
                               "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/SED_NoLaser_440_600_run012_15-02-22.txt", \
                                   "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Spectrum data - 15.2/energy_data.txt", False)

plt.figure(figsize=(12,6))
plt.errorbar(lambdas1, css1, uncs1)
plt.errorbar(lambdas2, css2, uncs2)
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