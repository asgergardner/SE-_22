import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat

def test_analysis(data_laser, data_nolaser, plot):
    def cs(Na, Nb, Na0, Nb0, wl, E_pulse):
        return (Na - Na0*Nb/Nb0) / (Nb*E_pulse/(1/wl))
    
    def unc(Na, Nb, Na0, Nb0, wl, E_pulse, E_pulse_unc):
        return np.sqrt(Na*(1/(Nb*E_pulse*wl))**2 + Na0*(-1/(E_pulse*Nb0*wl))**2 \
            + Nb*(-Na/(E_pulse*wl)*1/Nb**2)**2 \
                + Nb0*(-Na0/(E_pulse*wl)*1/Nb0**2)**2 \
                    + E_pulse_unc**2*(-(Na-Nb*Na0/Nb0)/(Nb*wl*E_pulse**2))**2)

    mcp_nolaser = np.loadtxt(data_nolaser, delimiter=",")
    ts = np.linspace(0,12000, len(mcp_nolaser))

    mcp_laser = np.loadtxt(data_laser, delimiter=",")
    lambdas = np.linspace(410, 700, len(mcp_laser))
    
    E_pulse = np.ones(len(mcp_laser))
    E_pulse_unc = np.ones(len(E_pulse))*1e-1
    
    max_val = 0
    max_idx = 0
    for i in range(len(mcp_laser)):
        if max(mcp_laser[i]) > max_val:
            max_val = max(mcp_laser[i])
            max_idx = np.argmax(mcp_laser[i])
    
    if plot:
        plt.figure()
        plt.title("Background")
        plt.plot(ts, mcp_nolaser)
        plt.show()

    css = np.zeros(len(mcp_laser))
    uncs = np.zeros(len(mcp_laser))
    for i in range(len(mcp_laser)):
        if plot:
            plt.figure()
            plt.title(r"$\lambda$ = " + str(lambdas[i]))
            plt.plot(ts, mcp_laser[i])
            plt.vlines(ts[max_idx], 0, max(mcp_laser[i]), colors="red", linewidth=3)
            plt.vlines(ts[-1], 0, max(mcp_laser[i]), colors="red", linewidth=3)
            plt.hlines(0, ts[max_idx], ts[-1], colors="red", linewidth=3)
            plt.hlines(max(mcp_laser[i]), ts[max_idx], ts[-1], colors="red", linewidth=3)
            plt.vlines(ts[700], 0, max(mcp_laser[i]), color="green", linewidth=3)
            plt.vlines(ts[max_idx-200], 0, max(mcp_laser[i]), color="green", linewidth=3)
            plt.hlines(0, ts[700], ts[max_idx-200], color="green", linewidth=3)
            plt.hlines(max(mcp_laser[i]), ts[700], ts[max_idx-200], color="green", linewidth=3)
            plt.show()
        
        Na = sum(mcp_laser[i][max_idx:-1])
        Nb = sum(mcp_laser[i][700:(max_idx-200)])
        Na0 = sum(mcp_nolaser[max_idx:-1])
        Nb0 = sum(mcp_nolaser[700:(max_idx-200)])
        wl = lambdas[i]
        
        css[i] = cs(Na, Nb, Na0, Nb0, wl, E_pulse[i])
        uncs[i] = unc(Na, Nb, Na0, Nb0, wl, E_pulse[i], E_pulse_unc[i])

    #uncs = np.zeros(len(css))
    fig = plt.figure()
    plt.errorbar(lambdas, css, uncs)
    plt.show()
    
    return fig

cross1 = test_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_Laser_410-700_run001_15-02-22.txt", "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_NoLaser_410-700_run001_15-02-22.txt", False)
cross2 = test_analysis("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/SED_Laser_410-700_run001_15-02-22.txt", "C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/SED_NoLaser_410-700_run001_15-02-22.txt", False)