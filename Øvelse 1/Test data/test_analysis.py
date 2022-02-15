import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat

def cs(Na, Nb, Na0, Nb0, wl, E_pulse):
    return (Na - Na0*Nb/Nb0) / (Nb*E_pulse/(1/wl))

mcp_nolaser = np.loadtxt("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_NoLaser_410-700_run001_15-02-22.txt", delimiter=",")
ts = np.linspace(0,12000, len(mcp_nolaser))
plt.plot(ts, mcp_nolaser)

mcp_laser = np.loadtxt("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 1/Test data/MCP_Laser_410-700_run001_15-02-22.txt", delimiter=",")
lambdas = np.linspace(410, 700, len(mcp_laser))

max_val = 0
max_idx = 0
for i in range(len(mcp_laser)):
    if max(mcp_laser[i]) > max_val:
        max_val = max(mcp_laser[i])
        max_idx = np.argmax(mcp_laser[i])

css = np.zeros(len(mcp_laser))
for i in range(len(mcp_laser)):
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
    E_pulse = 1
    
    css[i] = cs(Na, Nb, Na0, Nb0, wl, E_pulse)
    
plt.plot(lambdas, css, ".")