#!/usr/bin/env python
#%%
import numpy as np, pandas as pd
from netCDF4 import Dataset
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.signal import savgol_filter

homedir = '/home/mlicer/projects/podnebnik/SSH/'
sshfile = '{}SLR_total.csv'.format(homedir)

ssh = pd.read_csv(sshfile,parse_dates=['date'])
ssh = ssh.set_index(['date'])
ssh  =ssh.drop(['ssh_rcp26', 'ssh_rcp45','rcp45_mean','ssh_rcp85','rcp85_mean'],axis=1)

#low pass filter:
ssh['historical_rollmean_15yr'] = savgol_filter(ssh['ssh_historical'],15, 2, mode='nearest')
ssh['tot_rcp85_rollmean_15yr'] = savgol_filter(ssh['tot_rcp85'],15, 2, mode='nearest')
ssh['tot_rcp45_rollmean_15yr'] = savgol_filter(ssh['tot_rcp45'],15, 2, mode='nearest')

figname='{}Total_SSH_RCP85_RCP45.pdf'.format(homedir)
lwidth=3
lwidth2=5
alpha=0.4
plt.close()
plt.figure(figsize=(15,15))
plt.title('MSLR in Northern Adriatic')
plt.plot(ssh.index,ssh['ssh_historical'],'k', linewidth=lwidth, label='MedCordex Reanalysis')# %%
plt.plot(ssh.index,ssh['historical_rollmean_15yr'],'k', linewidth=lwidth2, alpha= alpha, label='15yr Rolling Mean Historical SSH')# %%
plt.plot(ssh.index,ssh['tot_rcp85'],'orangered', linewidth=lwidth, label='Total SSH RCP8.5')# %%
plt.plot(ssh.index,ssh['tot_rcp85_rollmean_15yr'],'orangered', linewidth=lwidth2, alpha=alpha, label='15yr Rolling Mean RCP8.5')# %%
plt.plot(ssh.index,ssh['tot_rcp45'],'steelblue', linewidth=lwidth, label='Total SSH RCP4.5')# %%
plt.plot(ssh.index,ssh['tot_rcp45_rollmean_15yr'],'steelblue', linewidth=lwidth2, alpha=alpha,label='15yr Rolling Mean RCP4.5')# %%
plt.xlabel('Year')
plt.ylabel('MSLR [m]')
plt.grid()
plt.legend()
plt.savefig(figname,dpi=300,bbox_inches='tight')

ssh.to_csv('{}MSLR_North_Adriatic_2100_RCP85_RCP45.csv'.format(homedir))
# %%
