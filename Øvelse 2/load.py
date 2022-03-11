import numpy as np
import matplotlib.pyplot as plt

def load(filename):
    # Open, read and close
    text_file = open(filename, "r")
    raw = text_file.read()
    text_file.close()
    
    # Split in header and data
    text = raw.split("[AndorNewton]")
    header = text[0]
    data = text[1]
    
    # Find excitation wavelength
    temp = header.split("Excitation wavelength: ")
    temp2 = temp[1].split(" nm")
    wl = float(temp2[0])
    
    # Read data and put into table
    rows = data.split("\n")
    tab = np.zeros((len(rows), 4))
    for i in range(len(rows)):
        vals = rows[i].split("\t")
        if vals != ['']:
            tab[i,0] = float(vals[0])
            tab[i,1] = float(vals[1])
            tab[i,2] = float(vals[2])
            tab[i,3] = float(vals[3])        
    
    return wl, tab[1:-1]

# Just to illustrate the functionality    
wl, tab = load("C:/Users/soere/Dropbox/Skoleting/8. semester/Store Eksperimentelle Øvelser/SE-_22/Øvelse 2/Raw data files/Fluorescence/22030803_LUNA.dat")
plt.plot(tab[:,0], tab[:,3])