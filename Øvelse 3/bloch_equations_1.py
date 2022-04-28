import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def B1_sq(t, tau, omega1, pulse_shape):
    tau_end = tau + pulse_shape/omega1
    if t>tau and t<tau_end:
        return omega1
    else:
        return 0
    

def bloch(var, t, tau, omega1, pulse_shape, T1, T2, M0):
    Mx, My, Mz = var
    R1 = 1/T1
    R2 = 1/T2
    
    dMxdt = -R2*Mx
    dMydt = B1_sq(t, tau, omega1, pulse_shape)*Mz - R2*My
    dMzdt = -B1_sq(t, tau, omega1, pulse_shape)*My - R1*(Mz - M0)
    
    return [dMxdt, dMydt, dMzdt]

t0 = 0
t1 = 1
ts = np.linspace(t0, t1, 10001)

T1 = 1000
T2 = 1000
M0 = 1
omega1 = 10
tau = 0.2

pulse_shape = np.pi
B1s = [B1_sq(ts[i], tau, omega1, pulse_shape) for i in range(len(ts))]

plt.figure()
plt.plot(ts,B1s)
plt.xlabel("t")
plt.ylabel(r"B$_1$(t)")
if pulse_shape == np.pi/2 : plt.title(r"$\pi/2$ pulse")
if pulse_shape == np.pi : plt.title(r"$\pi$ pulse")
plt.grid()
plt.show()

M_init = [1,1,1]

res1 = np.array(odeint(bloch, M_init, ts, args=(tau, omega1, pulse_shape, T1, T2, M0)))

plt.figure()
plt.plot(ts, res1[:,0])
plt.plot(ts, res1[:,1])
plt.plot(ts, res1[:,2])
plt.xlabel("Time")
plt.ylabel("Magnetization")
if pulse_shape == np.pi/2 : plt.title(r"$\pi/2$ pulse")
if pulse_shape == np.pi : plt.title(r"$\pi$ pulse")
plt.legend(["Mx", "My", "Mz"])
plt.grid()
plt.show()