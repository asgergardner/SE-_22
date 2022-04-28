import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def bloch_solver(M_init, T1, T2, omega1, dOmega, phi, T, pulse_shape, plot):
    
    def B1_sq(t, tau, omega1, pulse_shape):
        tau_end = tau + pulse_shape/omega1
        if t>tau and t<tau_end:
            return omega1
        else:
            return 0
    

    def bloch(var, t, tau, omega1, pulse_shape, T1, T2, M0, phi, dOmega):
        Mx, My, Mz = var
        R1 = 1/T1
        R2 = 1/T2
        
        gamma = 1
        
        B1 = B1_sq(t, tau, omega1, pulse_shape)
        c = np.cos(phi)
        s = np.sin(phi)
        
        dMxdt = gamma*(My*dOmega/gamma - Mz*B1*s) - R2*Mx
        dMydt = gamma*(Mz*B1*c - Mx*dOmega/gamma) - R2*My
        dMzdt = gamma*(Mx*B1*s - My*B1*c) - R1*(Mz - M0)
        
        return [dMxdt, dMydt, dMzdt]

    t0 = 0
    t1 = T
    ts = np.linspace(t0, t1, 10001)
    
    M0 = 1
    tau = 0.2
    
    if plot:
        B1s = [B1_sq(ts[i], tau, omega1, pulse_shape) for i in range(len(ts))]
        plt.figure(figsize=(12,7))
        plt.plot(ts,B1s)
        plt.xlabel("Time $t$", fontsize=16)
        plt.ylabel(r"Applied magnetic field $B_1(t)$", fontsize=16)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        if pulse_shape == np.pi/2 : plt.title(r"$\pi/2$ pulse", fontsize=20)
        if pulse_shape == np.pi : plt.title(r"$\pi$ pulse", fontsize=20)
        plt.grid()
        plt.show()

    res = np.array(odeint(bloch, M_init, ts, args=(tau, omega1, pulse_shape, T1, T2, M0, phi, dOmega)))

    Mx = res[:,0]
    My = res[:,1]
    Mz = res[:,2]
    
    if plot:
        plt.figure(figsize=(12,7))
        plt.plot(ts, Mx)
        plt.plot(ts, My)
        plt.plot(ts, Mz)
        plt.xlabel("Time $t$", fontsize=16)
        plt.ylabel("Magnetization $M_{x,y,z}$", fontsize=16)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        if pulse_shape == np.pi/2 : plt.title(r"$\pi/2$ pulse", fontsize=20)
        if pulse_shape == np.pi : plt.title(r"$\pi$ pulse", fontsize=20)
        plt.legend([r"$M_x$", r"$M_y$", r"$M_z$"], fontsize=16)
        plt.grid()
        plt.show()
    return [Mx, My, Mz]

M_init = [0.5,0,1]
T1 = 1000
T2 = 1000
omega1 = 10
dOmega = 0
phi = 0
T = 1
pulse_shape = np.pi/2
plot = True

Mx, My, Mz = bloch_solver(M_init, T1, T2, omega1, dOmega, phi, T, pulse_shape, plot)