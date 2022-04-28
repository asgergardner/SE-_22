import numpy as np
import matplotlib.pyplot as plt
from math import isclose

def sweep(tw, nz, b1, plot, integrate):
    
    def B1(t, tw, nz, b1):
        trf = nz*tw
        if -trf/2 < t and t < trf/2:
            return b1*np.sin(2*np.pi*t/tw)/(2*np.pi*t/tw)
        else:
            return 0

    t0 = -5
    t1 = 5
    ts = np.linspace(t0, t1, 10000)
    
    while(True):
        B1s = [B1(ts[i], tw, nz, b1) for i in range(len(ts))]
        area = np.trapz(B1s, dx = ts[1]-ts[0])
        if isclose(area, np.pi/2, abs_tol=1e-3):
            break
        else: 
            b1 = b1 + 1e-4
            print(b1)

    if plot:
        B1s = [B1(ts[i], tw, nz, b1) for i in range(len(ts))]

        plt.figure()
        plt.plot(ts,B1s)
        plt.xlabel("t")
        plt.ylabel(r"B$_1$(t)")
        plt.grid()
        plt.show()
        
    if integrate:
        area = np.trapz(B1s, dx = ts[1]-ts[0])
        return b1, area
    
    else:
            return b1, None

tw = 1
nz = 1
b1 = 2.5# Initial guess

b1, area = sweep(tw, nz, b1, True, True)