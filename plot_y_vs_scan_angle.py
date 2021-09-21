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
    filepath = 'c_gw_downlink_axial_ratio_RHCP_phi'+str(scan_phi[i])+'.csv'
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
plt.savefig("axial_ratio_vs_scan_angle.png", dpi=150)

rg=0*np.ones((num_elevation_plane,num_scan_theta))
fig, ax = plt.subplots()
legend_list=[]
for i in range(num_elevation_plane):
    filepath = 'c_gw_downlink_realized_gain_RHCP_phi'+str(scan_phi[i])+'.csv'
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
plt.savefig("realized_gain_lhcp_vs_scan_angle.png", dpi=150)





# filepath = 'd1_opted_210908_rlhcp_phi0.csv'
# rlhcp0 = extract_y(filepath)

# filepath = 'd1_opted_210908_rtotal_phi0.csv'
# rtotal0 = extract_y(filepath)
# l = len(rtotal0)
# rworst0 = []
# for i in range(l):
#     wg = rtotal0[i] - 10*log10(1+10**(ar0[i]/10))
#     rworst0.append(wg)


# ####################################################################
# fig, ax = plt.subplots()
# plt.plot(scan_theta, ar0)
# plt.legend(('phi=0',),loc='lower left')
# plt.xlim([0, 60])
# plt.ylim([0,9])
# plt.grid()
# plt.xlabel('scan theta (degree)')
# plt.ylabel('axial ratio (dB)')
# plt.title('Axial Ratio (dB) vs. Scan Angle')
# plt.savefig("axial_ratio_vs_scan_angle.png", dpi=150)

# spec_theta = np.linspace(0,60,num=61)
# spec_rlhcp = 4+1.3*10*np.log10(np.cos(spec_theta/180*pi))
# fig, ax = plt.subplots()
# plt.plot(scan_theta, rlhcp0)
# plt.plot(spec_theta, spec_rlhcp, 'k--')
# plt.legend(('phi=0','gain spec'),loc='lower left')
# plt.xlim([0, 60])
# plt.ylim([0,5])
# plt.grid()
# plt.xlabel('scan theta (degree)')
# plt.ylabel('realized LHCP gain (dB)')
# plt.title('Realized LHCP Gain (dB) vs. Scan Angle')
# plt.savefig("realized_lhcp_vs_scan_angle.png", dpi=150)


# spec_theta = np.linspace(0,60,num=61)
# spec_rlhcp = 4+1.3*10*np.log10(np.cos(spec_theta/180*pi))-3
# fig, ax = plt.subplots()
# plt.plot(scan_theta, rworst0)
# plt.plot(spec_theta, spec_rlhcp, 'k--')
# plt.legend(('phi=0','gain spec (assuming Tx. AR=0)'),loc='lower left')
# plt.xlim([0, 60])
# plt.ylim([-5,2])
# plt.grid()
# plt.xlabel('scan theta (degree)')
# plt.ylabel('worst gain seen by iPhone (dB)')
# plt.title('Realized Worst Gain (dB) vs. Scan Angle')
# plt.savefig("realized_worst_gain_vs_scan_angle.png", dpi=150)