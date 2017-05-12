

import matplotlib
matplotlib.use('GTK')


from getdist import plots, MCSamples



import getdist

import numpy as np
import matplotlib.pyplot as plt 
import astropy 
from loadMontePython import load as loadMCMC
import glob

basedir = "/home/zequnl/Projects/isocurvature_2017/analysis/plot_triangle/nonzero/"

burnin = 1000
data1 = loadMCMC('planckdata/r1.txt', 'planckdata/param')
data2 = loadMCMC('planckdata/r2.txt', 'planckdata/param')
data = astropy.table.vstack( [data1[burnin:], data2[burnin:]])
data_planck = data[:]
weights_planck = data['acceptance'][:]
for col in ['likelihood', 'acceptance','omega_b','omega_cdm','100theta_s','tau_reio']:
	data.remove_column(col)

nparr_planck = np.array(data.as_array().tolist()[:])
planck_real = MCSamples(samples=nparr_planck,names = data.colnames, labels = data.colnames, name_tag='Actual Planck Data')


## A 
folder = basedir + 'fA/'
files = glob.glob(folder + "*__*.txt")
params = glob.glob(folder + "*_.paramnames")

datalist = []
for f in files:
	datalist.append(  loadMCMC(f, params[0]) )

data = astropy.table.vstack( datalist )
data_sim = data[:]
weights_act = data['acceptance'][:]
for col in ['likelihood', 'acceptance','omega_b','omega_cdm','100theta_s','tau_reio']:
	data.remove_column(col)
nparr_act = np.array(data.as_array().tolist()[:])
planck = MCSamples(samples=nparr_act,names = data.colnames, labels = data.colnames, name_tag='Forecasted Planck low_l TEB + high_l TT')




#Triangle plot
g = plots.getSubplotPlotter()
g.triangle_plot([ planck_real, planck], filled=True)

# now we add some boundaries

# P_II^1
for ax in g.subplots[:,2]:
	if ax != None:
		ax.set_xlim(0,ax.get_xlim()[1])

for ax in g.subplots[2,:]:
	if ax != None:
		ax.set_ylim(0,ax.get_ylim()[1])


# P_II^2
for ax in g.subplots[:,3]:
	if ax != None:
		ax.set_xlim(0,ax.get_xlim()[1])


for ax in g.subplots[3,:]:
	if ax != None:
		ax.set_ylim(0,ax.get_ylim()[1])

plt.savefig('ONLY_planck.pdf')
plt.show()