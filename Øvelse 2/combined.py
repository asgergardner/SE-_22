from flourescence_analysis import flo_analysis
from absorption_analysis import abs_analysis
import matplotlib.pyplot as plt

wl_f, sig_f, uncs_f = flo_analysis(False)
wl_a, sig_a, uncs_a = abs_analysis(False, False)

plt.figure(figsize=(8,4))
plt.errorbar(wl_f, sig_f, uncs_f, marker=".", color="red", markersize=10, capsize=4)
plt.errorbar(wl_a, sig_a/(max(sig_a)/max(sig_f)), uncs_a/(max(sig_a)/max(sig_f)), marker=".", color="blue", markersize=10, capsize=4)
plt.xlabel("Wavelength [nm]", fontsize=14)
plt.ylabel("Yield [arb. units]", fontsize=14)
plt.xlim(558,615)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.rc('font', size=14)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.grid()
plt.locator_params(nbins=8)
plt.tick_params(bottom=True, top=True, right=True, left=True,
                direction="in", length=7, width=1.2)
plt.legend(["Flourescence spectrum","Absorption spectrum"], fontsize=14)
plt.show()

