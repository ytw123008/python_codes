# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 11:03:26 2022

@author: ytw19
"""

from math import *
import cmath as cmt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from matplotlib import animation

def ph_cal(xA, yA, f, theta0, phi0, eid=[]):
    '''
    This function calculates the phase to be assigned to the array elements
    Parameters----------
    xA : list of Array elements' x-coordinate [m] (row-wise)
    yA : list of Array elements' y-coordinate [m] (row-wise)
    f : freq. of the array [Hz]
    theta0,phi0 : scan angle [rad]
    eid : list of array element id
    Returns-------------
    phA : list of phases of each array element
    '''
    phA=[]
    c=3e8
    k0=2*pi/(c/f)
    kx0=k0*sin(theta0)*cos(phi0)
    ky0=k0*sin(theta0)*sin(phi0)
    for i in range(len(xA)):
        phA.append(-kx0*xA[i]-ky0*yA[i]) 
    return phA

def configA(a, b, gamma, 
            em=[], en=[], aper_based=False, aper_dia=0, aper_len=0, aper_width=0):
    '''
    Parameters----------
    a : element spacing along y-axis [m]
    b : row spacing along x-axis [m]
    gamma : array grid angle (rotate from y-axis) [rad]
    em,en : 2 lists of element's (m,n) coordinates
    aper_based : determine if the config is synthesized based on aperture size
    aper_dia : diameter of aperture if circularly-shaped [m]
    aper_len,aper_width : length and width of aperture if rectangular-shaped [m]
    Returns-------------
    xA, yA : 2 lists of element's (x,y) coordinates [m]
    '''
    xA = []
    yA = []
    if len(em)>0:
        assert aper_based==False
        for i in range(len(em)):
            xA.append(em[i]*b)
            yA.append(en[i]*a+em[i]*b/tan(gamma))
        assert len(xA)==len(em)
    else:
        assert aper_based==True and max(aper_dia,aper_len,aper_width)>0
        xA, yA = populate_A(a, b, gamma, aper_dia, aper_len, aper_width)
        
    
    # print(xA)
    return xA, yA

def populate_A(a, b, gamma, aper_dia, aper_len, aper_width):
    '''
    Parameters----------
    a : element spacing along y-axis [m]
    b : row spacing along x-axis [m]
    gamma : array grid angle (rotate from y-axis) [rad]
    aper_dia : diameter of aperture if circularly-shaped [m]
    aper_len,aper_width : length and width of aperture if rectangular-shaped [m]
    Returns-------------
    xA, yA : 2 lists of element's (x,y) coordinates [m]
    '''
    xA=[]
    yA=[]
    if aper_dia>0:
        m = np.linspace(-100,100,num=201,dtype=int)
        n = np.linspace(-100,100,num=201,dtype=int)
        for i in range(len(m)):
            for j in range(len(n)):
                if sqrt((m[i]*b)**2+(n[j]*a+m[i]*b/tan(gamma))**2)<aper_dia/2:
                    xA.append(m[i]*b)
                    yA.append(n[j]*a+m[i]*b/tan(gamma))
    if aper_len>0:
        assert aper_width>0
        m = np.linspace(-100,100,num=201,dtype=int)
        n = np.linspace(-100,100,num=201,dtype=int)
        for i in range(len(m)):
            for j in range(len(n)):
                if abs(m[i]*b)<aper_len/2 and abs(n[j]*a+m[i]*b/tan(gamma))<aper_width/2:
                    xA.append(m[i]*b)
                    yA.append(n[j]*a+m[i]*b/tan(gamma))
    return xA, yA

def af_cal(xA, yA, phA, f, sll, 
           # theta=np.linspace(0,90,num=91), phi=np.linspace(0,360,num=361)):
           u=np.linspace(-1,1,num=181), v=np.linspace(-1,1,num=181)):
    '''
    Parameters----------
    xA : list of Array elements' x-coordinate [m] (row-wise)
    yA : list of Array elements' y-coordinate [m] (row-wise)
    phA : list of Array elements' phase [rad] (row-wise)
    f : freq. of the array [Hz]
    sll : allowed sidelobe level
    Returns-------------
    af : 2d numpy array of array factors (u-v plane)
    af_dB : 2d numpy array of array factors [dB] (u-v plane)
    '''
    # af=np.zeros((len(theta),len(phi)),dtype=complex)
    # af_dB=np.zeros((len(theta),len(phi)),dtype=float)
    af=1e-1000000000*np.ones((len(u),len(v)),dtype=complex)
    af_dB=np.zeros((len(u),len(v)),dtype=float)
    # u = np.zeros((len(theta)*len(phi),),dtype=float)
    # v = np.zeros((len(theta)*len(phi),),dtype=float)
    k0=2*pi/(c/f)
    assert len(xA)==len(yA) and len(xA)==len(phA)
    # for m in range(len(theta)):
    #     for n in range(len(phi)):
    #         print('now theta is:'+str(theta[m]))
    #         print('now phi is:'+str(phi[n]))
    #         u[m,n] = sin(theta[m])*cos(phi[n])
    #         v[m,n] = sin(theta[m])*sin(phi[n])
    #         for i in range(len(xA)):
    #             ph_ele=k0*sin(theta[m])*cos(phi[n])*xA[i]+k0*sin(theta[m])*sin(phi[n])*yA[i]+phA[i]
    #             af[m,n]+=cmt.exp(1j*ph_ele)
    for m in range(len(u)):
        for n in range(len(v)):
            if (u[m]**2+v[n]**2)<=1:
                for i in range(len(xA)):
                    ph_ele=k0*u[m]*xA[i]+k0*v[n]*yA[i]+phA[i]
                    af[m,n]+=cmt.exp(1j*ph_ele)
    af_dB=20*np.log10(np.absolute(af))
    af_dB_norm = af_dB - np.amax(af_dB)
    af_dB_norm_th = af_dB_norm
    for m in range(len(u)):
        for n in range(len(v)):
            if af_dB_norm[m,n]<sll and af_dB_norm[m,n]>-1000000000:
                af_dB_norm_th[m,n]=sll
    return af, af_dB_norm, af_dB_norm_th, u, v

if __name__ == "__main__":
    global c
    c=3e8
    
    fs = 2.5e9
    theta0s = 60*pi/180
    phi0s = 45*pi/180
    gamma = 60*pi/180
    a_s = 61.76e-3
    b_s = a_s*sin(gamma)
    xAs, yAs = configA(a_s, b_s, gamma, aper_based=True,aper_len=1.75,aper_width=1.75)
    phAs = ph_cal(xAs, yAs, fs, theta0s, phi0s)
    sll = -30
    af,af_dB_norm, af_dB_norm_th, u, v = af_cal(xAs, yAs, phAs, fs, sll)
    assert len(phAs)==len(xAs)
    print(len(xAs))
    
    # f = 1.6265e9
    # theta0l = 60*pi/180
    # phi0l = 45*pi/180
    # gamma = 60*pi/180
    # a_l = a_s*sqrt(3)
    # b_l = a_l*sin(gamma)
    # xAl, yAl = configA(a_l, b_l, gamma, aper_based=True,aper_len=1.75,aper_width=1.75)
    # phAl = ph_cal(xAl, yAl, f, theta0l, phi0l)
    # assert len(phAl)==len(xAl)
    # print(len(xAl))
    
    # fig, ax = plt.subplots(figsize=(15, 15))
    # ax.scatter(yAl,xAl,s=250,color='grey')
    # ax.scatter(xAs,yAs,s=50,color='black')
    # ax.set_xlabel(r'x(m)', fontsize=15)
    # ax.set_ylabel(r'y(m)', fontsize=15)
    # plt.xlim([-1,1])
    # plt.ylim([-1,1])
    # plt.savefig('interwoven_config_ls.png',dpi=150)
    
    fig, ax = plt.subplots(figsize=(19, 15))
    U,V=np.meshgrid(u,v)
    plt.contourf(u, v, af_dB_norm_th,50)
    plt.colorbar()
    
    
    # f = 2.5e9
    # gamma = 60*pi/180
    # a = 61.761e-3
    # b = a*sin(gamma)
    # em = [-1,-1,0,0,0,1,1]
    # en = [0,1,-1,0,1,-1,0]
    # xA, yA = configA(a, b, gamma, em, en)
    # print(xA)
    # print(yA)
    # theta0 = 50*pi/180
    # phi0 = 30*pi/180
    # phA = ph_cal(xA, yA, f, theta0, phi0)
    # print(phA)
    
    
    # fig, ax = plt.subplots(figsize=(15, 15))
    # ax.scatter(xA,yA,s=250,color='black')
    # ax.set_xlabel(r'x(m)', fontsize=15)
    # ax.set_ylabel(r'y(m)', fontsize=15)
    # # plt.xlim([-1,1])
    # # plt.ylim([-1,1])
    # # plt.savefig('interwoven_config_ls.png',dpi=150)
