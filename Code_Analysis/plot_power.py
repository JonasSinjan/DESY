import matplotlib.pyplot as plt
import numpy as np

n = 128

dir_data = "/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_displacement/128run2D_73_paratest/power_spectra/"  # data files
dir_output = "/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_displacement/128run2D_73_paratest/power_spectra/"

# perpendicular
filename = dir_data + 'PS_KT_PHI.DAT'
ps_kperp = np.loadtxt(filename)
log_ps_kperp = [np.log(i) for i in ps_kperp[:,1] if i.any() != 0]

# parallel
filename = dir_data + 'PS_KB_PHI.DAT'
ps_kpar = np.loadtxt(filename)
log_ps_kpar = [np.log(i) for i in ps_kpar[:,1] if i.any() != 0]

#print(len(log_ps_kperp))S
#print(len(log_ps_kpar))

#print(log_ps_kpar)
#print(log_ps_kperp)

logk = np.log(range(n/2))

#print(len(logk))

p0_perp = np.polyfit(logk, log_ps_kperp[1:], 1)
p0_para = np.polyfit(logk, log_ps_kpar[1:], 1)

print(p0_para, p0_perp)

plt.figure()
plt.plot(logk, log_ps_kperp[1:], label='Kperp')
plt.plot(logk, log_ps_kpar[1:], label = 'Kpara')
plt.legend()
plt.show()