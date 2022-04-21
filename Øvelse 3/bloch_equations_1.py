import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def bloch(var, t, T, pulse_shape, T1, T2, M0):
    Mx, My, Mz = var
    R1 = 1/T1
    R2 = 1/T2
    
    omega1 = pulse_shape/T
    
    dMxdt = -R2*Mx
    dMydt = omega1*Mz - R2*My
    dMzdt = -omega1*My - R1*(Mz - M0)
    
    return [dMxdt, dMydt, dMzdt]

t0 = 0
t1 = 1


ts = np.linspace(t0, t1, 10001)
M_init = [1/2,1/2,1/2]

T1 = 1000
T2 = 1000
omega1 = 1
M0 = 1

res1 = np.array(odeint(bloch, M_init, ts, args=(t1, np.pi/2, T1, T2, M0)))
res2 = np.array(odeint(bloch, M_init, ts, args=(t1, np.pi, T1, T2, M0)))


plt.figure()
plt.plot(ts, res1[:,0])
plt.plot(ts, res1[:,1])
plt.plot(ts, res1[:,2])
plt.plot(ts, res2[:,0], "--")
plt.plot(ts, res2[:,1])
plt.plot(ts, res2[:,2])
plt.xlabel("Time")
plt.ylabel("Magnetization")
plt.legend(["Mx - pi/2", "My - pi/2", "Mz - pi/2", "Mx - pi", "My - pi", "Mz - pi"])
plt.grid()
plt.show()