import numpy as np

def bloch(var, t, T, b1, T1, T2, M0):
    Mx, My, Mz = var
    R1 = 1/T1
    R2 = 1/T2
    
    def B1(t, b1, tw, nz):
        trf = nz*tw
        if(-0.5*trf < t  and t < 0.5*trf):
            return b1 * np.sin(2*np.pi*t/tw)/(2*np.pi*t/tw)
        else:
            return 0
        
    gamma = 2.675e8
    tw = 1
    nz = 1
    
    omega1 = gamma*B1(t,b1,tw,nz)
    
    dMxdt = -R2*Mx
    dMydt = omega1*Mz - R2*My
    dMzdt = -omega1*My - R1*(Mz - M0)
    
    return [dMxdt, dMydt, dMzdt]



