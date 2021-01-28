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

def plot_field_on_map(lon2,lat2,time,field2d,figname):

	lonmin=np.min(lon2)
	lonmax=np.max(lon2)
	latmin=np.min(lat2)
	latmax=np.max(lat2)

	fig=plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
	ax.set_extent([lonmin, lonmax, latmin, latmax], ccrs.PlateCarree())
	ax.coastlines('10m')
	im=ax.pcolor(lon2, lat2,field2d)

	# ax.add_feature(cartopy.feature.OCEAN, zorder=0)
	ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')	
	plt.colorbar(im,ax=ax,shrink=0.75)
	print(time)
	plt.title(datetime.strftime(time,'%d %b %Y %H:%M'))
	# ax.xlabels_top = False
	# ax.ylabels_right=False
	gl=ax.gridlines(draw_labels=True,alpha=0.5, linestyle='--')
	gl.top_labels=gl.right_labels=False
	# ax.xlines = True	
	plt.savefig(figname,dpi=300,bbox_inches='tight')
	print('Saved {}.'.format(figname))

homedir='/home/mlicer/projects/podnebnik/'
ncfile='{}tmp.nc'.format(homedir)

lon = read_nc_var(ncfile,'lon')
lat = read_nc_var(ncfile,'lat')
time = read_nc_datetimes(ncfile,'time')
SST = read_nc_var(ncfile,'thetao')

lon2,lat2=np.meshgrid(lon,lat)

timestep=0
timestr = datetime.strftime(time[timestep],'%Y%m%d_%H%M')
print(timestr)
figname='{}CMEMS_SST_{}.pdf'.format(homedir,timestr)
plot_field_on_map(lon2,lat2,time[timestep],SST,figname)


