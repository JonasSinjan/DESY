import matplotlib.pyplot as plt
import numpy as np
#import read,amrplot
from matplotlib import ticker
from matplotlib import gridspec
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline
from scipy.stats import linregress

def smoothing(xarr) :
  lls = xarr.size
  smoothx = np.zeros(lls)
  smoothx[0] = xarr[0]
  smoothx[lls-1] = xarr[lls-1]
  for i in range (1,lls-1) :
    smoothx[i] = 0.25*xarr[i-1]+0.5*xarr[i]+0.25*xarr[i+1]
  return smoothx

def lppcorr(llv,sfpar,sfperp) :
  lls = sfpar.size
  lperp_arr = np.zeros(lls)
  lpar_arr = np.zeros(lls)
  count = 0
  for i in range (1,lls) :
    lpar = i*1.0
    stfc = sfpar[i]
    if (stfc > np.amax(sfperp) or stfc < np.amin(sfperp)) : 
      continue
    #trying to find the ll for which sf_par matches the value of stfc
    for j in range (0,lls-1) :
      if ((sfperp[j] < stfc) and (sfperp[j+1] >= stfc)) : # this is where the 2d_squares struc funk fails because the sfperp[j+1] >= sfpar[i] for all (all decrease)
        xll = llv[j]+((llv[j+1]-llv[j])/(sfperp[j+1]-sfperp[j]))*(stfc-sfperp[j])
        break
    lperp_arr[count] = xll
    lpar_arr[count]  = lpar
    count = count+1  
  return [lperp_arr,lpar_arr]


def read_sf(dir_data, n):
  filename = dir_data
  lentf= n
  data = np.loadtxt(filename,skiprows=1)
  ll = data[:,0]
  sf_par = data[:,1]
  sf_perp= data[:,2]
  valid = ~np.isnan(sf_perp)
  sf_perp = sf_perp[valid]
  ll = ll[valid]
  sf_par = sf_par[valid]
  lent = np.size(ll)
  sf_par_smoothed = smoothing(sf_par)
  sf_perp_smoothed= smoothing(sf_perp)
  [lperpe,lpyare] = lppcorr(ll,sf_par_smoothed,sf_perp_smoothed)
  lpar = lpyare/lentf
  lperp = lperpe/lentf

  return lpar, lperp

def find_indeix(arr): #normally pass through the perp array: lperp
  for count, i in enumerate(arr):
    if  i <= 0.0001:
      return count #returns the index where 0 starts
      break

perp_arr,para_arr = [], []

def linfit(perp_arr, para_arr, count):
  slope, intercept, rval, p, err = linregress(np.log(perp_arr[:count]), np.log(para_arr[:count]))
  tmp_slop = round(slope,3)
  tmp_r = round(rval,3)
  tmp_err = round(err,3)
  return tmp_slop, tmp_r, tmp_err


#--------------------------------------------------------------------------------------------------------------------------------------------
# Reading SF data
#--------------------------------------------------------------------------------------------------------------------------------------------


#PHI

# #2d displacement sf phi
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/128run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar1, lperp1 = read_sf(dir_sf, 128.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/256run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar2, lperp2 = read_sf(dir_sf, 256.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/512run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar3, lperp3 = read_sf(dir_sf, 512.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/1024run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar8, lperp8 = read_sf(dir_sf, 1024.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/2048run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar9, lperp9 = read_sf(dir_sf, 2048.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/4096run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar16, lperp16 = read_sf(dir_sf, 4096.0)

# #2d_squares sf rho(=phi) 
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/square_128run2D/sf_par_perp_v_phiF.txt'
# lpar10, lperp10 = read_sf(dir_sf, 128.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/square_256run2D/sf_par_perp_v_phiF.txt'
# lpar11, lperp11 = read_sf(dir_sf, 256.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/square_512run2D/sf_par_perp_v_phiF.txt'
# lpar12, lperp12 = read_sf(dir_sf, 512.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/square_1024run2D/sf_par_perp_v_phiF.txt'
# lpar13, lperp13 = read_sf(dir_sf, 1024.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/square_2048run2D/sf_par_perp_v_phiF.txt'
# lpar14, lperp14 = read_sf(dir_sf, 2048.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_sq_vs_disp_data/square_4096run2D/sf_par_perp_v_phiF.txt'
# lpar15, lperp15 = read_sf(dir_sf, 4096.0)

# # #3d displacement sf phi
# # dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/128run2D_FFT/sf_par_perp_v_phiF.txt'
# # lpar20, lperp20 = read_sf(dir_sf, 128.0)
# # #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/256run2D_FFT/sf_par_perp_v_phiF.txt'
# lpar21, lperp21 = read_sf(dir_sf, 256.0)
# #
# # filename = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/512run2D_FFT/sf_par_perp_v_phiF.txt'
# # lpar22, lperp22 = read_sf(dir_sf, 512.0)

# #PHI0

# # #2d displacement sf phi0 wrt global
# # dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/128run2D_FFT/sf_par_perp_v_phi0F_wrt_global.txt'
# # lpar17, lperp17 = read_sf(dir_sf, 128.0)
# # #
# # dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/256run2D_FFT/sf_par_perp_v_phi0F_wrt_global.txt'
# # lpar18, lperp18 = read_sf(dir_sf, 256.0)
# #
# # filename = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/512run2D_FFT/sf_par_perp_v_phi0F.txt'
# # lpar19, lperp19 = read_sf(dir_sf, 512.0)

# #3d displacement sf phi0 wrt global
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/128run3D_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
# lpar23, lperp23 = read_sf(dir_sf, 128.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/256run3D_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
# lpar24, lperp24 = read_sf(dir_sf, 256.0)
# #
# # filename = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/512run2D_FFT/sf_par_perp_v_phiF.txt'
# # lpar25, lperp25 = read_sf(dir_sf, 512.0)

# #3d displacement sf phi0 wrt local
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/128run3D_FFT/sf_par_perp_v_phi0F.txt'
# lpar26, lperp26 = read_sf(dir_sf, 128.0)
# #
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/2d_vs_3d_data/256run3D_FFT/sf_par_perp_v_phi0F.txt'
# lpar27, lperp27 = read_sf(dir_sf, 256.0)

# #3d displacement real init phi0
# dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/3d_displacement/128run3D/sf_par_perp_v_phi0F.txt'
# lpar28, lperp28 = read_sf(dir_sf, 128.0)

#-------------------------------------------------------------------------------------------------------------
# reading final data
#-------------------------------------------------------------------------------------------------------------

working_dir_path = '/home/jonas/Documents/VSCode/DESY/'

# 2d

# #displacement
# #real - 512
# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/512run2D_disp_real/sf_par_perp_v_phi0_wrt_globalF.txt'
# dir_sf = working_dir_path + 'final_data/2d/512run2D_disp_real/sf_par_perp_v_phi0_wrt_globalF.txt'
# lpar1, lperp1 = read_sf(dir_sf, 512.0)

# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/512run2D_disp_real/sf_par_perp_v_phi0_wrt_localF.txt'
# dir_sf = working_dir_path + 'final_data/2d/512run2D_disp_real/sf_par_perp_v_phi0_wrt_localF.txt'
# lpar2, lperp2 = read_sf(dir_sf, 512.0)

# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/512run2D_disp_real/sf_par_perp_v_phiF.txt'
# dir_sf = working_dir_path + 'final_data/2d/512run2D_disp_real/sf_par_perp_v_phiF.txt'
# lpar3, lperp3 = read_sf(dir_sf, 512.0)

# #fft
# #256
# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/256run2D_disp_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
# dir_sf = working_dir_path + 'final_data/2d/256run2D_disp_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
# lpar4, lperp4 = read_sf(dir_sf, 256.0)

# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/256run2D_disp_FFT/sf_par_perp_v_phiF.txt'
# dir_sf = working_dir_path + 'final_data/2d/256run2D_disp_FFT/sf_par_perp_v_phiF.txt'
# lpar5, lperp5 = read_sf(dir_sf, 256.0)

# #512
# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/512run2D_disp_FFT/sf_par_perp_v_phi0F.txt' #should check
# dir_sf = working_dir_path + 'final_data/2d/512run2D_disp_FFT/sf_par_perp_v_phi0F.txt'
# lpar6, lperp6 = read_sf(dir_sf, 512.0)

# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/512run2D_disp_FFT/sf_par_perp_v_phiF.txt'
# dir_sf = working_dir_path + 'final_data/2d/512run2D_disp_FFT/sf_par_perp_v_phiF.txt'
# lpar7, lperp7 = read_sf(dir_sf, 512.0)

# #squares
# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/2d/512run2D_sq/sf_par_perp_v_phiF.txt'
# dir_sf = working_dir_path + 'final_data/2d/512run2D_sq/sf_par_perp_v_phiF.txt'
# lpar8, lperp8 = read_sf(dir_sf, 512.0)

#3d

#displacement
#real
#64
# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/3d/64run3D_real/sf_par_perp_v_F.txt' #need to check if actually phi
# dir_sf = working_dir_path + 'final_data/3d/64run3D_real/sf_par_perp_v_F.txt'
# lpar9, lperp9 = read_sf(dir_sf, 64.0)

# #dir_sf = '/lustre/fs23/group/that/jonas/Github_repo/DESY/final_data/3d/64run3D_real/sf_par_perp_v_phi0F.txt'
# dir_sf = working_dir_path + 'final_data/3d/64run3D_real/sf_par_perp_v_phi0F.txt'
# lpar10, lperp10 = read_sf(dir_sf, 64.0)

#128
dir_sf = working_dir_path + 'final_data/3d/128run3D_real/sf_par_perp_v_phi0_wrt_globalF.txt'
lpar11, lperp11 = read_sf(dir_sf, 128.0)

dir_sf = working_dir_path + 'final_data/3d/128run3D_real/sf_par_perp_v_phiF.txt'
lpar12, lperp12 = read_sf(dir_sf, 128.0)

#fft - 256
dir_sf = working_dir_path + 'final_data/3d/256run3D_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
lpar13, lperp13 = read_sf(dir_sf, 256.0)

dir_sf = working_dir_path + 'final_data/3d/256run3D_FFT/sf_par_perp_v_phiF.txt'
lpar14, lperp14 = read_sf(dir_sf, 256.0)
 
#fft-128
dir_sf = working_dir_path + 'final_data/3d/128run3D_FFT/sf_par_perp_v_phiF.txt'
lpar15, lperp15 = read_sf(dir_sf, 128.0)


dir_sf = working_dir_path + 'final_data/3d/128run3D_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
lpar16, lperp16 = read_sf(dir_sf, 128.0)

#phi0 wrt local
dir_sf = working_dir_path + 'final_data/3d/128run3D_real/sf_par_perp_v_phi0_wrt_localF.txt'
lpar17, lperp17 = read_sf(dir_sf, 128.0)

dir_sf = working_dir_path + 'final_data/3d/128run3D_FFT/sf_par_perp_v_phi0_wrt_localF.txt'
lpar18, lperp18 = read_sf(dir_sf, 128.0)

dir_sf = working_dir_path + 'final_data/3d/256run3D_FFT/sf_par_perp_v_phi0_wrt_localF.txt'
lpar19, lperp19 = read_sf(dir_sf, 256.0)

#fft-512
dir_sf = working_dir_path + 'final_data/3d/512run3D_mem_FFT/sf_par_perp_v_phiF.txt'
lpar20, lperp20 = read_sf(dir_sf, 512.0)

dir_sf = working_dir_path + 'final_data/3d/512run3D_mem_FFT/sf_par_perp_v_phi0_wrt_globalF.txt'
lpar21, lperp21 = read_sf(dir_sf, 512.0)

#phi0 wrt local
dir_sf = working_dir_path + 'final_data/3d/512run3D_mem_FFT/sf_par_perp_v_phi0_wrt_localF.txt'
lpar22, lperp22 = read_sf(dir_sf, 512.0)


#--------------------------------------------------------------------------------------------------------------------------------------------
# Finding index at which sf becomes 0
#--------------------------------------------------------------------------------------------------------------------------------------------


#perp and para - data becomes 0 at some point, run into errors, so want to find point that they become 0 and stop at that point

# #2d displacement phi
# count_128disp = find_indeix(lperp1)
# #
# count_256disp = find_indeix(lperp2)
# #
# count_512disp = find_indeix(lperp3)
# #
# count_1024disp = find_indeix(lperp8)
# #
# count_2048disp = find_indeix(lperp9)
# #
# count_4096disp = find_indeix(lperp16)

# #2d squares rho(=phi)
# count_128sq = find_indeix(lperp10)
# #
# count_256sq = find_indeix(lperp11)
# #
# count_512sq = find_indeix(lperp12)
# #
# count_1024sq = find_indeix(lperp13)
# #
# count_2048sq = find_indeix(lperp14)
# #
# count_4096sq = find_indeix(lperp15)

# # #2d displacement phi0
# # count_128disp_phi0 = find_indeix(lperp17)
# # #
# # count_256disp_phi0 = find_indeix(lperp18)
# # #
# # count_512disp_phi0 = find_indeix(lperp19)
# # #

# # #3d displacement phi
# # count_128disp_3dphi = find_indeix(lper20)
# # #
# count_256disp_3dphi = find_indeix(lperp21)
# #
# # count_512disp_phi = find_indeix(lperp22)
# # #

# #3d displacement phi0 real init
# count_128disp_3dphi0_real = find_indeix(lperp28)

# #3d displacement phi0 wrt global
# count_128disp_3dphi0 = find_indeix(lperp23)
# #
# count_256disp_3dphi0 = find_indeix(lperp24)
# #
# # count_512disp_phi0 = find_indeix(lperp25)
# # #

# #3d displacement phi0 wrt local
# count_128disp_3dphi0_loc = find_indeix(lperp26)
# #
# count_256disp_3dphi0_loc = find_indeix(lperp27)
#

# #2d displacement phi
# count_512disp = find_indeix(lperp1)

# #2d squares phi
# count_512sq= find_indeix(lperp8)

#3d displacement phi0
count_1283d_phi0 = find_indeix(lperp11)

#3d displacement phi
count_1283d = find_indeix(lperp12)

#3d displacement phi0 fft
count_256_3d_phi0f = find_indeix(lperp13)

#3d displacement phi fft
count_256_3d_f = find_indeix(lperp14)

#3d displacement phi fft
count_128_3d_f = find_indeix(lperp15)

#3d displacement phi0 fft
count_128_3d_phi0f = find_indeix(lperp16)

#3d displacement phi0 real
count_128_3d_phi0r_local = find_indeix(lperp17)

#3d displacement phi0 fft
count_128_3d_phi0f_local = find_indeix(lperp18)

#3d displacement phi0 fft 256
count_256_3d_phi0f_local = find_indeix(lperp19)

#3d displacement 512 phi 
count_512_3d_phi = find_indeix(lperp20)

#3d displacement 512 phi0 global
count_512_3d_phi0 = find_indeix(lperp21)

#3d displacement 512 phi0 local
count_512_3d_phi0_local = find_indeix(lperp22)

#--------------------------------------------------------------------------------------------------------------------------------------------
# ALL linefitting
#--------------------------------------------------------------------------------------------------------------------------------------------


# #slopes linefitting for 2d displacement phi
# slope_128_disp, rval_128_disp, err_128_disp = linfit(lperp1,lpar1, count_128disp)
# slope_256_disp, rval_256_disp, err_256_disp = linfit(lperp2,lpar2, count_256disp)
# slope_512_disp, rval_512_disp, err_512_disp = linfit(lperp3,lpar3, count_512disp)
# slope_1024_disp, rval_1024_disp, err_1024_disp = linfit(lperp8,lpar8, count_1024disp)
# slope_2048_disp, rval_2048_disp, err_2048_disp = linfit(lperp9,lpar9, count_2048disp)
# slope_4096_disp, rval_4096_disp, err_4096_disp = linfit(lperp16,lpar16, count_4096disp)

# #slope linefitting for 2d squares rho (=phi)
# slope_512_sq, rval_512_sq, err_512_sq = linfit(lperp12,lpar12, count_512disp)
# slope_1024_sq, rval_1024_sq, err_1024_sq = linfit(lperp13,lpar13, count_1024disp)
# slope_2048_sq, rval_2048_sq, err_2048_sq = linfit(lperp14,lpar14, count_2048sq)
# slope_4096_sq, rval_4096_sq, err_4096_sq = linfit(lperp15,lpar15, count_4096sq)

# # #slope linefitting 2d displacement phi0 wrt global
# # slope_128_disp_phi0, rval_128_disp_phi0, err_128_disp_phi0 = linfit(lperp17,lpar17, count_128disp_phi0)
# # slope_256_disp_phi0, rval_256_disp_phi0, err_256_disp_phi0 = linfit(lperp18,lpar18, count_256disp_phi0)

# #slope linefit 2d displacement real init
# slope_128_disp_3dphi0_real, rval_128_disp_3dphi0_real, err_128_disp_3dphi0_real = linfit(lperp28,lpar28, count_128disp_3dphi0_real)

# #slope linefitting 3d displacement phi0 wrt global
# fit_end = 20
# slope_128_disp_3dphi0, rval_128_disp_3dphi0, err_128_disp_3dphi0 = linfit(lperp23,lpar23, fit_end)
# slope_256_disp_3dphi0, rval_256_disp_3dphi0, err_256_disp_3dphi0 = linfit(lperp24,lpar24, fit_end) #count_256disp_3dphi0)

# #slope linefitting 3d displacement phi0 wrt local
# fit_end = 20
# slope_128_disp_3dphi0_loc, rval_128_disp_3dphi0_loc, err_128_disp_3dphi0_loc = linfit(lperp26,lpar26, fit_end)
# slope_256_disp_3dphi0_loc, rval_256_disp_3dphi0_loc, err_256_disp_3dphi0_loc = linfit(lperp27,lpar27, fit_end) #count_256disp_3dphi0)

# #slope linefitting 3d displacement phi wrt local
# fit_end = 20
# slope_256_disp_3dphi, rval_256_disp_3dphi, err_256_disp_3dphi = linfit(lperp21,lpar21, fit_end) #count_256disp_3dphi0)

#Reference slopes

# ref_slope_2_3 = lpar8[100]*(np.power(lperp8[:count_1024disp],(2.0/3.0))/np.power(lperp8[100],(2.0/3.0)))
# slope_ref, rval_ref, err_ref = linfit(lperp8, ref_slope_2_3, count_1024disp)

# ref_slope_2_3 = lpar16[100]*(np.power(lperp16[:count_4096disp],(2.0/3.0))/np.power(lperp16[100],(2.0/3.0)))
# slope_ref, rval_ref, err_ref = linfit(lperp16, ref_slope_2_3, count_4096disp)
#ref_slope_1 = lpar4[3]*(np.power(lperp4,(3.0/3.0))/np.power(lpar4[3],(3.0/3.0)))

# ref_slope_2_3 = lpar1[20]*(np.power(lperp1[:count_512disp],(2.0/3.0))/np.power(lperp1[20],(2.0/3.0)))
# ref_slope_2_3_sq = lpar8[10]*(np.power(lperp8[:count_512sq],(2.0/3.0))/np.power(lperp8[10],(2.0/3.0)))
#slope_ref, rval_ref, err_ref = linfit(lperp8, ref_slope_2_3, count_1024disp)
ref_slope_2_3_3d = lpar12[6]*(np.power(lperp12[:count_1283d],(2.0/3.0))/np.power(lperp12[6],(2.0/3.0)))

ref_slope_3d_128_f = lpar15[6]*(np.power(lperp15[:count_128_3d_f],(2.0/3.0))/np.power(lperp15[6],(2.0/3.0)))
ref_slope_3d_256_f = lpar14[6]*(np.power(lperp14[:count_256_3d_f],(2.0/3.0))/np.power(lperp14[6],(2.0/3.0)))


# #2d displacement 512
# slope_512_disp, rval_512_disp, err_512_disp = linfit(lperp1,lpar1, count_512disp)

# #2d sq 512
# slope_512_sq, rval_512_sq, err_512_sq = linfit(lperp8,lpar8, count_512sq)

#3d displacement 128 real
slope_128_disp, rval_128_disp, err_128_disp = linfit(lperp12,lpar12, count_1283d)

#3d displacement 128 fft
slope_128_disp_f, rval_128_disp_f, err_128_disp_f = linfit(lperp15,lpar15, count_128_3d_f)

#3d displacement 256 fft
slope_256_disp_f, rval_256_disp_f, err_256_disp_f = linfit(lperp14,lpar14, count_256_3d_f)

#3d displacement 128 real phi0
slope_128_disp_phi0, rval_128_disp_phi0, err_128_disp_phi0 = linfit(lperp11,lpar11, count_1283d_phi0)

#3d displacement 128 fft phi0
slope_128_disp_phi0f, rval_128_disp_phi0f, err_128_disp_phi0f = linfit(lperp16,lpar16, count_128_3d_phi0f)

#3d displacement 256 fft phi0
slope_256_disp_phi0f, rval_256_disp_phi0f, err_256_disp_phi0f = linfit(lperp13,lpar13, count_256_3d_phi0f)

#3d displacement 128 real phi0 local
slope_128_disp_phi0_local, rval_128_disp_phi0_local, err_128_disp_phi0_local = linfit(lperp17,lpar17, count_128_3d_phi0r_local)

#3d displacement 128 fft phi0 local
slope_128_disp_phi0f_local, rval_128_disp_phi0f_local, err_128_disp_phi0f_local = linfit(lperp18,lpar18, count_128_3d_phi0f_local)

#3d displacement 256 fft phi0 local
slope_256_disp_phi0f_local, rval_256_disp_phi0f_local, err_256_disp_phi0f_local = linfit(lperp19,lpar19, count_256_3d_phi0f_local)

#3d displacement 512 fft phi
slope_512_disp_3d_phi, rval_512_disp_3d_phi, err_512_disp_3d_phi = linfit(lperp20,lpar20, count_512_3d_phi)

#3d displacement 512 fft phi0 global
slope_512_disp_3d_phi0, rval_512_disp_3d_phi0, err_512_disp_3d_phi0 = linfit(lperp21,lpar21, count_512_3d_phi0)

#3d displacement 512 fft phi0 local
slope_512_disp_3d_phi0_local, rval_512_disp_3d_phi0_local, err_512_disp_3d_phi0_local = linfit(lperp22,lpar22, count_512_3d_phi0_local)

#--------------------------------------------------------------------------------------------------------------------------------------------
# 2d squares vs displacement phi PLOT
#--------------------------------------------------------------------------------------------------------------------------------------------



# plt.figure(figsize=(9.0, 5.0), dpi=200)
# gs = gridspec.GridSpec(1, 1, hspace=0.0, wspace=0.0)

# ax0 = plt.subplot(gs[0])

# # #2D displacement phi
# # ax0.plot(lperp1[:count_128disp], lpar1[:count_128disp], lw=3, ls = "-", label="128_2D_disp grad: %s R^2: %s  Err: %s" % (slope_128_disp, rval_128_disp, err_128_disp))
# # ax0.plot(lperp2[:count_256disp], lpar2[:count_256disp], lw=3, ls = "-", label="256_2D_disp grad: %s R^2: %s  Err: %s" % (slope_256_disp, rval_256_disp, err_256_disp))
# # ax0.plot(lperp3[:count_512disp], lpar3[:count_512disp], lw=3, ls = "-", label="512_2D_disp grad: %s R^2: %s  Err: %s" % (slope_512_disp, rval_512_disp, err_512_disp))
# #ax0.plot(lperp8[:count_1024disp], lpar8[:count_1024disp], lw=3, ls = "-", label="1024_2D_disp grad: %s R^2: %s  Err: %s" % (slope_1024_disp, rval_1024_disp, err_1024_disp))
# #ax0.plot(lperp9[:count_2048disp], lpar9[:count_2048disp], lw=3, ls = "-", label="2048_2D_disp grad: %s R^2: %s  Err: %s" % (slope_2048_disp, rval_2048_disp, err_2048_disp))
# #ax0.plot(lperp16[:count_4096disp], lpar16[:count_4096disp], lw=3, ls = "-", label="4096_2D_disp grad: %s R^2: %s  Err: %s" % (slope_4096_disp, rval_4096_disp, err_4096_disp))

# ax0.plot(lperp1[:count_512disp], lpar1[:count_512disp], lw=5, ls = "-", label="512_disp_real grad: %s R^2: %s  Err: %s" % (slope_512_disp, rval_512_disp, err_512_disp))

# # # #2D squares rho(=phi)
# # # #ax0.plot(lperp12[:count_512sq], lpar12[:count_512sq], lw=5, ls = ":", label="512_2D_sq grad: %s R^2: %s  Err: %s" % (slope_512_sq, rval_512_sq, err_512_sq))
# #ax0.plot(lperp13[:count_1024sq], lpar13[:count_1024sq], lw=5, ls = ":", label="1024_2D_sq grad: %s R^2: %s  Err: %s" % (slope_1024_sq, rval_1024_sq, err_1024_sq))
# #ax0.plot(lperp14[:count_2048sq], lpar14[:count_2048sq], lw=5, ls = ":", label="2048_2D_sq grad: %s R^2: %s  Err: %s" % (slope_2048_sq, rval_2048_sq, err_2048_sq))
# #ax0.plot(lperp14[:count_4096sq], lpar14[:count_4096sq], lw=5, ls = "-", label="4096_2D_sq grad: %s R^2: %s  Err: %s" % (slope_4096_sq, rval_4096_sq, err_4096_sq))

# ax0.plot(lperp8[:count_512sq], lpar8[:count_512sq], lw=5, ls = "-.", label="512_squares grad: %s R^2: %s  Err: %s" % (slope_512_sq, rval_512_sq, err_512_sq))

# #ax0.plot(lperp16[:count_4096disp], ref_slope_2_3, lw=6, color = "black", ls = "-", label="GS95 grad: %s R^2: %s  Err: %s" % (slope_ref, rval_ref, err_ref))
# # ax0.plot(lperp8[:count_1024disp], ref_slope_2_3, lw=6, color = "black", ls = "-", label="GS95 grad: %s R^2: %s  Err: %s" % (slope_ref, rval_ref, err_ref))

# ax0.plot(lperp1[:count_512disp], ref_slope_2_3, lw=4, color = "black", ls = "-", label="GS95 2/3") # grad: %s R^2: %s  Err: %s" % (slope_ref, rval_ref, err_ref))
# ax0.plot(lperp8[:count_512sq], ref_slope_2_3_sq, lw=4, color = "black", ls = "-")#, label="GS95 2/3") # grad: %s R^2: %s  Err: %s" % (slope_ref, rval_ref, err_ref))
# ax0.set_xscale('log')
# ax0.set_yscale('log')
# #ax0.set_xlim(xmax=0.3)
# #ax0.set_ylim(ymax=0.5)
# #sort out scales max - these were all phi wrt to magnetic field
# ax0.set_xlabel(r'$l_{\perp}/ L $ perpendicular',fontsize=18)
# ax0.set_ylabel('$l_{\parallel}/L $ parallel',fontsize=18)
# ax0.set_title('Structure Function 2D Displacement vs Squares')
# ax0.legend(loc='lower right',ncol=1,fontsize=12)

# plt.show()

# #2d vs 3d real
# plt.figure(figsize=(9.0, 5.0), dpi=200)
# gs = gridspec.GridSpec(1, 1, hspace=0.0, wspace=0.0)

# ax0 = plt.subplot(gs[0])

# ax0.plot(lperp1[:count_512disp], lpar1[:count_512disp], lw=5, ls = "-", label="2D 512 grad: %s R^2: %s  Err: %s" % (slope_512_disp, rval_512_disp, err_512_disp))

# ax0.plot(lperp12[:count_1283d], lpar12[:count_1283d], lw=5, ls = "-.",color = "red", label="3D 128 grad: %s R^2: %s  Err: %s" % (slope_128_disp, rval_128_disp, err_128_disp))

# ax0.plot(lperp1[:count_512disp], ref_slope_2_3, lw=4, color = "black", ls = "-", label="GS95 2/3")
# ax0.plot(lperp12[:count_1283d], ref_slope_2_3_3d, lw=4, color = "black", ls = "-")

# ax0.set_xscale('log')
# ax0.set_yscale('log')
# ax0.set_xlabel(r'$l_{\perp}/ L $ perpendicular',fontsize=18)
# ax0.set_ylabel(r'$l_{\parallel}/L $ parallel',fontsize=18)
# ax0.set_title('Structure Function 2D vs 3D Displacement Real PHI')
# ax0.legend(loc='lower right',ncol=1,fontsize=12)

# plt.show()

#3d fft vs real phi
plt.figure(figsize=(9.0, 5.0), dpi=200)
gs = gridspec.GridSpec(1, 1, hspace=0.0, wspace=0.0)

ax1 = plt.subplot(gs[0])



ax1.plot(lperp12[:count_1283d], lpar12[:count_1283d], lw=5, ls = "-.",color = "red", label="128 Real grad: %s R^2: %s  Err: %s" % (slope_128_disp, rval_128_disp, err_128_disp))

ax1.plot(lperp15[:count_128_3d_f], lpar15[:count_128_3d_f], lw=5, ls = "-",color = "green", label="128 FFT grad: %s R^2: %s  Err: %s" % (slope_128_disp_f, rval_128_disp_f, err_128_disp_f))

ax1.plot(lperp14[:count_256_3d_f], lpar14[:count_256_3d_f], lw=5, ls = "--",color='orange', label="256 FFT grad: %s R^2: %s  Err: %s" % (slope_256_disp_f, rval_256_disp_f, err_256_disp_f))

#ax1.plot(lperp14[:count_256_3d_f], ref_slope_3d_256_f, lw=4, color = "black", ls = "-", label="GS95 2/3")
ax1.plot(lperp12[:count_1283d], 1.5*ref_slope_2_3_3d, lw=4, color = "black", ls = "-", label="GS95 2/3")
#ax1.plot(lperp15[:count_128_3d_f], ref_slope_3d_128_f, lw=4, color = "black", ls = "-")


ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel(r'$l_{\perp}/ L $ perpendicular',fontsize=18)
ax1.set_ylabel(r'$l_{\parallel}/L $ parallel',fontsize=18)
ax1.set_title('Structure Function 3D Disp. Real vs FFT PHI')
ax1.legend(loc='lower right',ncol=1,fontsize=13)

plt.show()


#3d fft vs real phi0
plt.figure(figsize=(5.0, 3.0), dpi=200)
gs = gridspec.GridSpec(1, 1, hspace=0.0, wspace=0.0)

ax1 = plt.subplot(gs[0])



#ax1.plot(lperp11[:count_1283d_phi0], lpar11[:count_1283d_phi0], lw=2, ls = "-.",color = "red", label="128 Real grad: %s R^2: %s  Err: %s" % (slope_128_disp_phi0, rval_128_disp_phi0, err_128_disp_phi0))

ax1.plot(lperp16[:count_128_3d_phi0f], lpar16[:count_128_3d_phi0f], lw=2, ls = "-",color = "green", label="128 FFT grad: %s R^2: %s  Err: %s" % (slope_128_disp_phi0f, rval_128_disp_phi0f, err_128_disp_phi0f))

ax1.plot(lperp13[:count_256_3d_phi0f], lpar13[:count_256_3d_phi0f], lw=2, ls = "--",color='orange', label="256 FFT grad: %s R^2: %s  Err: %s" % (slope_256_disp_phi0f, rval_256_disp_phi0f, err_256_disp_phi0f))

#ax1.plot(lperp17[:count_128_3d_phi0r_local], lpar17[:count_128_3d_phi0r_local], lw=2, ls = "-.",color = "red", label="128 Real grad: %s R^2: %s  Err: %s" % (slope_128_disp_phi0_local, rval_128_disp_phi0_local, err_128_disp_phi0_local))

#ax1.plot(lperp18[:count_128_3d_phi0f_local], lpar18[:count_128_3d_phi0f_local], lw=2, ls = "-",color = "green", label="128 FFT grad: %s R^2: %s  Err: %s" % (slope_128_disp_phi0f_local, rval_128_disp_phi0f_local, err_128_disp_phi0f_local))

#ax1.plot(lperp19[:count_256_3d_phi0f_local], lpar19[:count_256_3d_phi0f_local], lw=2, ls = "--",color='orange', label="256 FFT grad: %s R^2: %s  Err: %s" % (slope_256_disp_phi0f_local, rval_256_disp_phi0f_local, err_256_disp_phi0f_local))

#ax1.plot(lperp20[:count_512_3d_phi], lpar20[:count_512_3d_phi], lw=2, ls = "-.",color = "red", label="512 Phi grad: %s R^2: %s  Err: %s" % (slope_512_disp_3d_phi, rval_512_disp_3d_phi, err_512_disp_3d_phi))

ax1.plot(lperp21[:count_512_3d_phi0], lpar21[:count_512_3d_phi0], lw=2, ls = "-", label="512 Phi0 global grad: %s R^2: %s  Err: %s" % (slope_512_disp_3d_phi0, rval_512_disp_3d_phi0, err_512_disp_3d_phi0))

#ax1.plot(lperp22[:count_512_3d_phi0_local], lpar22[:count_512_3d_phi0_local], lw=2, ls = "--",color='orange', label="512 Phi0 local grad: %s R^2: %s  Err: %s" % (slope_512_disp_3d_phi0_local, rval_512_disp_3d_phi0_local, err_512_disp_3d_phi0_local))

#ax1.plot(lperp14[:count_256_3d_f], ref_slope_3d_256_f, lw=4, color = "black", ls = "-", label="GS95 2/3")
ax1.plot(lperp12[:count_1283d], 1.5*ref_slope_2_3_3d, lw=2, color = "black", ls = "-", label="GS95 2/3")
#ax1.plot(lperp15[:count_128_3d_f], ref_slope_3d_128_f, lw=4, color = "black", ls = "-")


ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel(r'$l_{\perp}/ L $ perpendicular',fontsize=9)
ax1.set_ylabel(r'$l_{\parallel}/L $ parallel',fontsize=9)
ax1.set_title('Structure Function 3D Disp. FFT PHI0 wrt global')
ax1.legend(loc='lower right',ncol=1,fontsize=6)

plt.show()

#print(lperp3)
#print(lpar3)

#--------------------------------------------------------------------------------------------------------------------------------------------
# 2d vs 3d displacement phi & phi0 PLOT
#--------------------------------------------------------------------------------------------------------------------------------------------

#ref_slope_2_3 = lpar24[20]*(np.power(lperp24[:count_256disp_3dphi0],(2.0/3.0))/np.power(lperp24[20],(2.0/3.0)))
#slope_ref, rval_ref, err_ref = linfit(lperp24, ref_slope_2_3, count_256disp_3dphi0)


#plot for 2d vs 3d displacement method both phi and phi0
#fig=plt.figure(2)
#fig = plt.figure(figsize=(16.0, 16.0))
#gs = gridspec.GridSpec(1, 1, hspace=0.0, wspace=0.0)

#ax0 = plt.subplot(gs[0],aspect='equal')

#2D displacement PHI0
#ax0.plot(lperp17[:count_128disp_phi0], lpar17[:count_128disp_phi0], lw=3, ls = "-", label="128_2D_disp_PHI0 grad: %s R^2: %s  Err: %s" % (slope_128_disp_phi0, rval_128_disp_phi0, err_128_disp_phi0))
#ax0.plot(lperp18[:count_256disp_phi0], lpar18[:count_256disp_phi0], lw=3, ls = "-", label="256_2D_disp_PHI0 grad: %s R^2: %s  Err: %s" % (slope_256_disp_phi0, rval_256_disp_phi0, err_256_disp_phi0))

#3D displacement PHI0 wrt global
#ax0.plot(lperp23[:count_128disp_3dphi0], lpar23[:count_128disp_3dphi0], lw=3, ls = "-", label="128_3D_disp_PHI0 grad: %s R^2: %s  Err: %s" % (slope_128_disp_3dphi0, rval_128_disp_3dphi0, err_128_disp_3dphi0))
#ax0.plot(lperp24[:count_256disp_3dphi0], lpar24[:count_256disp_3dphi0], lw=3, ls = "-", label="256_3D_disp_PHI0_global grad: %s R^2: %s  Err: %s" % (slope_256_disp_3dphi0, rval_256_disp_3dphi0, err_256_disp_3dphi0))
#ax0.scatter(lperp24[fit_end-1], lpar24[fit_end-1], color='red',s=80, label = 'End of linear fit region')

#3D displacement PHI0 wrt local
#ax0.plot(lperp26[:count_128disp_3dphi0_loc], lpar26[:count_128disp_3dphi0_loc], lw=3, ls = "-", label="128_3D_disp_PHI0_local grad: %s R^2: %s  Err: %s" % (slope_128_disp_3dphi0_loc, rval_128_disp_3dphi0_loc, err_128_disp_3dphi0_loc))
#ax0.plot(lperp27[:count_256disp_3dphi0_loc], lpar27[:count_256disp_3dphi0_loc], lw=3, ls = "-", label="256_3D_disp_PHI0_local grad: %s R^2: %s  Err: %s" % (slope_256_disp_3dphi0_loc, rval_256_disp_3dphi0_loc, err_256_disp_3dphi0_loc))
#ax0.scatter(lperp27[fit_end-1], lpar27[fit_end-1], color='pink',s=80, label = 'End of linear fit region')

#3D displacement PHI wrt local
#ax0.plot(lperp21[:count_256disp_3dphi], lpar21[:count_256disp_3dphi], lw=3, ls = "-", label="256_3D_disp_PHI grad: %s R^2: %s  Err: %s" % (slope_256_disp_3dphi, rval_256_disp_3dphi, err_256_disp_3dphi))

#3D displacement PHI0 real init
#ax0.plot(lperp28[:count_128disp_3dphi0_real], lpar28[:count_128disp_3dphi0_real], lw=3, ls = "-", label="128_3D_disp_PHI0_real grad: %s R^2: %s  Err: %s" % (slope_128_disp_3dphi0_real, rval_128_disp_3dphi0_real, err_128_disp_3dphi0_real))

#ax0.plot(lperp24[:count_256disp_3dphi0], ref_slope_2_3, lw=2, color = "black", ls = "-", label="GS95 grad: %s R^2: %s  Err: %s" % (slope_ref, rval_ref, err_ref))

# ax0.set_xscale('log')
# ax0.set_yscale('log')
# ax0.set_xlim(xmin=0.005, xmax=0.3)
# ax0.set_ylim(ymin=0.005, ymax=0.5)
# ax0.set_xlabel(r'$l_{\perp}/ L $ perpendicular',fontsize=18)
# ax0.set_ylabel('$l_{\parallel}/L $ parallel',fontsize=18)
# ax0.set_title('Structure Function 3D Displacement')
# ax0.legend(loc='lower right',ncol=1,fontsize=14)




#ax1 = plt.subplot(gs[1],aspect='equal')

# #2D displacement PHI
# ax1.plot(lperp3[:count_128disp], lpar3[:count_128disp], lw=3, ls = "-", label="128_2D_disp_PHI grad: %s R^2: %s  Err: %s" % (slope_128_disp, rval_128_disp, err_128_disp))
# ax1.plot(lperp8[:count_256disp], lpar8[:count_256disp], lw=3, ls = "-", label="256_2D_disp_PHI grad: %s R^2: %s  Err: %s" % (slope_256_disp, rval_256_disp, err_256_disp))
# ax1.plot(lperp3[:count_512disp], lpar3[:count_512disp], lw=3, ls = "-", label="512_2D_disp_PHI grad: %s R^2: %s  Err: %s" % (slope_512_disp, rval_512_disp, err_512_disp))

# ax1.set_xlabel(r'$l_{\perp}/ L $ perpendicular',fontsize=18)
# ax1.set_ylabel(r'$l_{\parallel}/L $ parallel',fontsize=18)
# ax1.set_title('Struc Funk 2D vs 3D Displacement PHI')
# ax1.legend(loc='lower right',ncol=2,fontsize=14)




#plt.show()