import numpy as np
import matplotlib.pyplot as plt

def do_load(filename):
    # Open, read and close
    text_file = open(filename, "r")
    raw = text_file.read()
    text_file.close()
    
    # Split data
    raw2 = raw.split("BEGIN\n")[1]
    raw3 = raw2.split("\nEND")[0]
    raw4 = raw3.split("\n")
    
    # Save data into one matrix by splitting lines and entries
    res = []
    for line in raw4:
        res_temp = []
        entries = line.split("\t")
        for entry in entries:
            if entry != "":
                val = float(entry)
                res_temp.append(val)
        res.append(res_temp)
    
    # Convert pixels --> physical valuess
    Es_a = 0.00151123500000061
    Es_b = 12.6463908625
    degs_a = 0.0493421052631579 
    degs_b = -13.404

    
    Es_idx = np.arange(0,len(res[0]))
    degs_idx = np.arange(0,len(res))

    Es = Es_a*Es_idx + Es_b
    degs = degs_a*degs_idx + degs_b

    
    return Es, degs, np.array(res)
    

# Just to illustrate the functionality    
Es, degs, data = do_load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 4/Data/Au111.txt")

fig,ax=plt.subplots(1,1)
cp = ax.contourf(Es, degs, data)
fig.colorbar(cp)    
plt.ylim(-8,8)

