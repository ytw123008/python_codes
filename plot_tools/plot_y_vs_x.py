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
import matplotlib.colors as mcolors


def extract_y(filepath:str, columns:list)->list:
    data_input = pd.read_csv(filepath).to_numpy()
    y = data_input[:,1:]
    # for i in range(m):
    #     for j in range(1,n):
    #         y[i,j-1]=data_input[i,j]
    return y

def extract_x(filepath:str)->list:
    data_input = pd.read_csv(filepath).to_numpy()
    x = data_input[:,0]
    return x

def plot(x:list, y:list, x_label:str, y_lable:str, x_lim:list, y_lim:list, 
         legends:tuple=(), legends_loc:str='lower left', colors:list=[], title:str='', savepath:str=''):
    
    assert len(x) == len(y[0]), "lengths of x and y are not equal!!"
    fig, ax = plt.subplots()
    
    if len(colors)>0:
        assert len(colors) == len(y[0]), "lengths of colors and y are not equal!"
        for i in len(y):
            plt.plot(x, y[i], colors[i])
    else:
        plt.plot(x, y[i])
        
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_lable)
    
    if len(title)>0:
        plt.title(title)
    if len(legends)>0:
        plt.legend(legends,loc=legends_loc)
    if len(savepath)>0:
        plt.savefig('',dpi=150)
    
    return print("figure plot finished!")


if __name__ == '__main__':
    filepath = ''

