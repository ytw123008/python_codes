# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 21:18:04 2021

@author: ytw19
"""

from math import *
import cmath as cm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def extract_y(filepath,sample_freq):
    data_input = pd.read_csv(filepath).to_numpy()
    x = data_input[:,0]
    freq_pos = int(np.where(x == 2.49)[0])
    y = data_input[5,2:]
    # for i in range(m):
    #     for j in range(1,n):
    #         y[i,j-1]=data_input[i,j]
    return y


sample_freq=2.49
filepath = ''
ar=extract_y(filepath, sample_freq)
filepath = ''
rg_total=extract_y(filepath, sample_freq)

rotate_lp=np.linspace(0,360/180*pi,num=361)
m = len(rg_total)
n = len(rotate_lp)
rg = 1000*np.ones((m,n))
fig, ax = plt.subplots()
for i in range(m):
    for j in range(n):
        rg[i,j]=rg_total[i]-10*log10(1+10**(ar[i]/10))+10*log10(10**(ar[i]/10)*(cos(rotate_lp[j]))**2+(sin(rotate_lp[j]))**2)
    plt.plot(rotate_lp*180/pi, rg[i,:])
plt.plot(rotate_lp*180/pi,[1+1.3*10*log10(cos(60*pi/180))]*n,'k--')
plt.xlim([0, 360])
plt.ylim([-5,5])
plt.yticks([-5,-3,-1,1,3,5])
plt.xticks([0,45,90,135,180,225,270,315,360])
plt.grid()
plt.xlabel('')
plt.ylabel('''''')
plt.title(r'Realized Gain (dB) Seen by iPhone with $\theta_{scan}$=$60^{o}$')
plt.legend(('$\phi_{scan}$=$0^{o}$','$\phi_{scan}$=$45^{o}$','$\phi_{scan}$=$90^{o}$'
            ,'$\phi_{scan}$=$135^{o}$','$\phi_{scan}$=$180^{o}$','$\phi_{scan}$=$225^{o}$'
            ,'$\phi_{scan}$=$270^{o}$','$\phi_{scan}$=$315^{o}$','Assuming AR=0'),loc='upper right')
plt.savefig('',dpi=150)