#!/usr/bin/env python

import sys, os, re
from datetime import datetime, timedelta
from sys import exit as q
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib as mpl
plt.rcParams.update({
	"text.usetex": True,
	"font.family": "sans-serif",
	"font.sans-serif": ["Helvetica"]})

def read_nc_var(fname,var):
	ncid=Dataset(fname,'r')
	return(np.squeeze(ncid.variables[var][:]))

def read_nc_datetimes(ncfile,time_varname):
	nc_Dataset=Dataset(ncfile)
	t=nc_Dataset.variables[time_varname]
	t0 = t.units
	mt =re.findall(r'\d{4}-\d+-\d+',t0)
	if 'seconds' in t.units:
		return np.array([datetime.strptime(mt[0],'%Y-%m-%d') + timedelta(seconds=i) for i in t[:]])
	if 'minutes' in t.units:
		return np.array([datetime.strptime(mt[0],'%Y-%m-%d') + timedelta(seconds=60*i) for i in t[:]])		
	elif 'hours' in t.units:
		return np.array([datetime.strptime(mt[0],'%Y-%m-%d') + timedelta(hours=i) for i in t[:]])
	else:
		print("Unknown units in NetCDF file!")
		q()

def get_latlon_index(lon0,lat0,lon2,lat2):
	# Returns i,j indices of (lon0,lat0) point in a (lon2,lat2) grid.
	return np.argmin(np.abs(lon2[0,:]-lon0)),np.argmin(np.abs(lat2[:,0]-lat0))

homedir='/home/mlicer/projects/CMEMS_data/'
ncfile='{}tmp_1yr.nc'.format(homedir)

lon = read_nc_var(ncfile,'lon')
lat = read_nc_var(ncfile,'lat')
time = read_nc_datetimes(ncfile,'time')
SST = read_nc_var(ncfile,'thetao')

lon2,lat2=np.meshgrid(lon,lat)

# select point coordinates to plot:
lon0 = 13.5
lat0 = 44.0
# retrieve i,j index of this point:
i0,j0 = get_latlon_index(lon0,lat0,lon2,lat2)

figname='{}CMEMS_SST_timeseries.pdf'.format(homedir)

plt.plot(time,SST[:,j0,i0])
plt.title(r"SST [$^\circ$C] timeseries at point ({} E,{} N)".format(lon0,lat0)) 
plt.grid()
plt.savefig(figname,bbox_inches='tight')
print('Saved {}'.format(figname))
# plt.show()


