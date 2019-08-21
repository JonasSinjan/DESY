import numpy as np 
import struct
import math
import scipy.interpolate as spint
from multiprocessing import Pool


tinynum = 1.0E-12
n_theta_pts = 50

def kspec_funk(ff):

    print(ff)

    #looping over theta and phi angles in k space
    theta_array = np.linspace(0.0,np.pi/2.0,n_theta_pts)
    count = 0
    pwr_f = 0.0
    
    for theta in theta_array :
        kxx = phikperp[ff]*np.cos(theta) #kxx in that plane - actually ky and kz(perp)
        kyy = phikperp[ff]*np.sin(theta) 
        pont=(kxx,kyy)
        pwr_f = pwr_f + np.exp(logp_interp(pont))
        count=count+1
    
    #taking shell average
    pwr_f = pwr_f/count
    
    #multiplying by shell area to get 1D power 
    f_pow = pwr_f*2.0*np.pi*phikperp[ff]

    return [f_pow]

def slice_fft(sn,phi):
    fx2d = phi[:,:,sn]
    
    #calculating the FFT
    fxk = np.fft.rfftn(fx2d)
   
    #shifting the zero frequency to center
    fxk_shifted = np.fft.fftshift(fxk,axes=0) 
    
    #computing the power
    pfxk = np.real(fxk_shifted*np.conjugate(fxk_shifted))
 
    for ii in range (0,np.size(pfxk,0)) :
        for jj in range (0,np.size(pfxk,1)) :
            if (math.isinf(pfxk[ii,jj]) or math.isnan(pfxk[ii,jj]) or pfxk[ii,jj]<tinynum):
                pfxk[ii,jj] = tinynum

    pfxyzk = pfxk      

    #removing the Nyquist component
    pfxyzk_wn = pfxyzk[1:xpt,0:ypt/2] 

    return(pfxyzk_wn)


def k_perp_calculator(n,phi,phi0, dir_data):
    
    xpt=n
    ypt=n
    zpt=n
    Lx=1.0
    Ly=1.0
    Lz=1.0
   
    nzslices = 20
   
    mode='F'
    nprocs = 24
    nprocsfft = 24

    RGI = spint.RegularGridInterpolator

    phikperp = np.zeros(n/2)
    phipower_spec = np.zeros(n/2)
    f_power_spec = np.zeros(n/2)
    pfolded = np.zeros((xpt/2,ypt/2))
    logpfolded = np.zeros((xpt/2,ypt/2))

    pool = Pool(processes=nprocsfft) 
    oter = pool.map(slice_fft, np.arange(0,n,n/nzslices))
    fftslices = np.asarray(oter)
    pool.terminate()

    pk_slice = np.mean(fftslices,axis=0)

    #folding along the y axis
    pfolded[0,:] = pk_slice[xpt/2-1,:]
    for w in range (1,xpt/2):
        pfolded[w,:] = 0.5*(pk_slice[xpt/2-1+w,:]+pk_slice[xpt/2-1-w,:]) 

    #taking the log for easier interpolation
    logpfolded = np.log(pfolded)

    #defining the axes of the 3d spec array
    kxarr = np.linspace(0.0,(xpt/2-1)*2.0*np.pi,num=xpt/2)
    kyarr = np.linspace(0.0,(ypt/2-1)*2.0*np.pi,num=ypt/2)

    #making the interpolation function
    logp_interp = RGI(points=[kxarr,kyarr], values=logpfolded)

    #making the spectrum now
    #zero wavenumber is special case
    phikperp[0] = 0.0
    pont = (0.0,0.0)
    f_power_spec[0] = np.exp(logp_interp(pont))

    #looping over the higher wavenumbers
    for i in range (1,n/2) :
        phikperp[i] = i*2.0*np.pi

    pool = Pool(processes=nprocs) 
    kspecs = pool.map(kspec_funk, np.arange(1,n/2))
    sff = np.asarray(kspecs)
    pool.terminate()

    f_power_spec[1:] = sff[:,0]

    #writing the spectra to a file
    f=open(dir_data+mode+'_kperp_spec.txt','w')
    for i in range(0,n/2):
        value=str(phikperp[i]) +" "+str(f_power_spec[i])
        f.write(value+"\n")
        f.close()

    return f_power_spec