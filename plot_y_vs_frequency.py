# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:28:26 2021

@author: ytw19
"""

from math import *
import cmath as cm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def extract_y(filepath):
    data_input = pd.read_csv(filepath).to_numpy()
    y = data_input[:,1:]
    # for i in range(m):
    #     for j in range(1,n):
    #         y[i,j-1]=data_input[i,j]
    return y

def extract_x(filepath):
    data_input = pd.read_csv(filepath).to_numpy()
    x = data_input[:,0]
    return x







filepath = 'c_gw_downlink_axial_ratio_RHCP.csv'
ar = extract_y(filepath)
f = extract_x(filepath)
m,n=np.shape(ar)
fig, ax = plt.subplots()
# fig.legend(loc=7) 
for i in range(n):
    plt.plot(f, ar[:,i])
plt.xlim([6.875, 7.055])
plt.ylim([0,12])
plt.grid()
plt.xlabel('frequency (GHz)')
plt.ylabel('axial ratio (dB)')
plt.title(r'Axial Ratio (dB) vs. Frequency with $\theta_{scan}$=0,$75^{o}$')
# plt.legend(loc=(2.04,0))
plt.legend((r'broadside','$\phi_{scan}$=$0^{o}$','$\phi_{scan}$=$45^{o}$','$\phi_{scan}$=$90^{o}$'
            ,'$\phi_{scan}$=$135^{o}$','$\phi_{scan}$=$180^{o}$','$\phi_{scan}$=$225^{o}$'
            ,'$\phi_{scan}$=$270^{o}$','$\phi_{scan}$=$315^{o}$'),loc='lower left')
plt.savefig('c_gw_downlink_AR_vs_freq.png',dpi=150)


filepath = 'c_gw_downlink_realized_gain_RHCP.csv'
rg = extract_y(filepath)
f = extract_x(filepath)
m,n=np.shape(rg)
fig, ax = plt.subplots()
# fig.legend(loc=7) 
for i in range(n):
    plt.plot(f, rg[:,i])
f_spec=np.linspace(6.875,7.055,num=51)
rg_spec=(3+1.5*10*log10(cos(75*pi/180)))*np.ones((51,1))
plt.plot(f_spec, rg_spec, 'k--')
plt.xlim([6.875, 7.055])
plt.ylim([-10,5])
plt.grid()
plt.xlabel('frequency (GHz)')
plt.ylabel('realized gain RHCP (dB)')
plt.title(r'Realized Gain RHCP (dB) vs. Frequency with $\theta_{scan}$=0,$75^{o}$')
# plt.legend(loc=(2.04,0))
plt.legend((r'broadside','$\phi_{scan}$=$0^{o}$','$\phi_{scan}$=$45^{o}$','$\phi_{scan}$=$90^{o}$'
            ,'$\phi_{scan}$=$135^{o}$','$\phi_{scan}$=$180^{o}$','$\phi_{scan}$=$225^{o}$'
            ,'$\phi_{scan}$=$270^{o}$','$\phi_{scan}$=$315^{o}$','link budget spec.'),loc='lower left')
plt.savefig('c_gw_downlink_rgrhcp_vs_freq.png',dpi=150)

