# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 12:53:04 2021

@author: ytw19
"""

from math import *
import cmath as cm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def extract_y(filepath):
    y = []
    data_input = pd.read_csv(filepath).to_numpy()
    m,n=np.shape(data_input)
    for i in range(1,n):
        y.append(data_input[i-1,i])
    return y

def extract_x(filepath):
    data_input = pd.read_csv(filepath).to_numpy()
    x = data_input[:,0]
    return x

num_elevation_plane = 8
start_elePlane=0
end_elePlane=315
scan_phi=np.linspace(start_elePlane,end_elePlane,num=num_elevation_plane,dtype=int)
num_scan_theta=16

ar=1000*np.ones((num_elevation_plane,num_scan_theta))
fig, ax = plt.subplots()
legend_list=[]
for i in range(num_elevation_plane):
    filepath = ''+str(scan_phi[i])+'.csv'
    scan_theta = extract_x(filepath)
    ar[i,:] = extract_y(filepath)
    plt.plot(scan_theta, ar[i,:])
    legend='$\phi_{scan}$=$'+str(scan_phi[i])+'^{o}$'
    legend_list.append(legend)
plt.legend((legend_list),loc='lower left')
plt.xlim([0, 75])
plt.ylim([0,12])
plt.grid()
plt.xlabel('scan theta (degree)')
plt.ylabel('axial ratio (dB)')
plt.title('Axial Ratio (dB) vs. Scan Angle')
plt.savefig("", dpi=150)

rg=0*np.ones((num_elevation_plane,num_scan_theta))
fig, ax = plt.subplots()
legend_list=[]
for i in range(num_elevation_plane):
    filepath = ''+str(scan_phi[i])+'.csv'
    scan_theta = extract_x(filepath)
    rg[i,:] = extract_y(filepath)
    plt.plot(scan_theta, rg[i,:])
    legend='$\phi_{scan}$=$'+str(scan_phi[i])+'^{o}$'
    legend_list.append(legend)
theta_spec=np.linspace(0,75,num=76)
rg_spec=3+1.5*10*np.log10(np.cos(theta_spec*pi/180))
plt.plot(theta_spec, rg_spec,'k--')
legend_list.append('link budget spec.')
plt.legend((legend_list),loc='lower left')
plt.xlim([0, 75])
plt.ylim([-8,6])
plt.grid()
plt.xlabel('$\\theta_{scan}$ (degree)')
plt.ylabel('realized $gain_{RHCP}$ (dB)')
plt.title('Realized $Gain_{RHCP}$ (dB) vs. Scan Angle')
plt.savefig("", dpi=150)





