# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:34:36 2016

@author: SaiPhani
"""

"""Packages required to execute the program"""
import xlrd                                   #Reading input from an .xls file
import os.path                                #Reading input from an .xls file
import matplotlib.pyplot as plt               #For plotting curves
from matplotlib.widgets import Slider         #For implementing Threshold Slider
import numpy as np                            #For Interpolation Techniques of Curve Fitting
import math                                   #For absolute value computation
from scipy.interpolate import interp1d        #Interpolation techniques 

"""Global variables"""
X_Coordinates = []                            #Wavelength (angs) values
Y_Coordinates = []                            #(Raw - OB)/OB values
alpha_list = []                               #Normalized Absolute Differences Sum 
beta_list = []                                #Sum of Absolute Differences of adjacent elements of each alpha_list element 
total_Span = 0                                #Total window width or length: 2*window_Span 


"""Method to read input dataset (Wavelength (angs) values and (Raw - OB)/OB values) into X_Coordinates and Y_Coordinates"""
def read_Input():
    wb = xlrd.open_workbook(os.path.join('Si_plot.xlsx'))
    wb.sheet_names()
    sh = wb.sheet_by_index(0)
    for i in range(1,1486):
        if sh.cell(i,6).value>=1.4 and sh.cell(i,6).value<=4.4:   #Considering Wavelength values that are in [1.4, 4.4] 
            X_Coordinates.append(sh.cell(i,6).value)
            Y_Coordinates.append(sh.cell(i,3).value)
    return 0

"""Method to capture Normalized Absolute Differences Sum of each element in Y_Coordinates a.k.a (Raw - OB)/OB values""" 
def construct_Alphalist(window_Span):
    for i in range(0, len(X_Coordinates)):
        temp_Sum = 0                #Intermediate Sum Value
        count = 0                   #Count to Normalize Absolute Differences Sum
        for j in range(0, len(X_Coordinates)):
            if X_Coordinates[j] >= X_Coordinates[i]-window_Span and X_Coordinates[j] <= X_Coordinates[i]+window_Span and Y_Coordinates[j]!=Y_Coordinates[i]:
                count += 1                
                temp_Sum  += math.fabs(Y_Coordinates[i] - Y_Coordinates[j])        
        alpha_list.append(temp_Sum/float(count))
    return 0
    
"""Method to populate beta_list elements"""
def construct_Betalist():
    beta_list.append(math.fabs(alpha_list[0]-alpha_list[1]))    
    
    for i in range(0, len(alpha_list)):        
        if i-1 >= 0 and i+1 < len(alpha_list):
            beta_list.append(math.fabs(alpha_list[i]-alpha_list[i-1])+math.fabs(alpha_list[i]-alpha_list[i+1]))

    beta_list.append(math.fabs(alpha_list[-1]-alpha_list[-2]))
    return 0
        
"""Method to smooth the curve where beta_list elements exceed the threshold limit""" 
def smoothing_Plot(total_Span, threshold):
    X_Smooth1   = []            #List to hold all the beta_listelements greater than threshold
    X_Smooth2   = []            #List to hold all the adjoining elements that fall into the window length of each element in X_Smooth1, including them
    temp_listX  = []            #List to hold all the elements of X_Coordinates that fall into window length of each element in X_Smooth2
    temp_listY  = []            #List to hold all the elements of Y_Coordinates that fall into window length of each element in X_Smooth2
    Smooth_X_Coordinates = []   #Smoothed Values of each element in X_Smooth2
    Smooth_Y_Coordinates = []   #Smoothed Values of each element in X_Smooth2
    
    for i in beta_list:
        if i > threshold:
            X_Smooth1.append(X_Coordinates[beta_list.index(i)])

    for i in X_Smooth1:
        for j in X_Coordinates:
            if j >= i-total_Span and j <= i+total_Span:
                X_Smooth2.append(j)

    for i in X_Coordinates:        
        if i in X_Smooth2:
            temp_listX = []
            temp_listY = []    
            for j in X_Coordinates:
                if j >= i-total_Span and j <= i+total_Span:        
                    temp_listX.append(j)
                    temp_listY.append(Y_Coordinates[X_Coordinates.index(j)])            
            Smooth_X_Coordinates.append(sum(temp_listX)/len(temp_listX))
            Smooth_Y_Coordinates.append(sum(temp_listY)/len(temp_listY))            
        else:
            Smooth_X_Coordinates.append(i)
            Smooth_Y_Coordinates.append(Y_Coordinates[X_Coordinates.index(i)])               

        
    interpolation(threshold,  X_Smooth1, Smooth_X_Coordinates, Smooth_Y_Coordinates)
    
    
"""Method for curve fitting the somoothed curve"""
def interpolation(threshold, X_Smooth1, Smooth_X_Coordinates, Smooth_Y_Coordinates):        
    threshold_List = [ threshold for i in range(len(X_Coordinates))]
    Smooth_X_npy = np.asarray(Smooth_X_Coordinates)
    Smooth_Y_npy = np.asarray(Smooth_Y_Coordinates)
    f = interp1d(Smooth_X_npy, Smooth_Y_npy, kind = "cubic" )
    xnew = np.linspace(Smooth_X_npy[0], Smooth_X_npy[len(Smooth_X_npy)-1], num = 3000, endpoint=True)

    plt.close('all')
    fig, ax = plt.subplots(5)
    fig.suptitle("Neutron Imaging Curve Smoothing", fontsize="x-large")

    ax[0] = plt.subplot2grid((6,7), (0,0), rowspan=2, colspan=3)
    ax[0].plot(X_Coordinates, Y_Coordinates)
    ax[0].set_title('Original Plot')
    
    ax[1] = plt.subplot2grid((6,7), (3,0), rowspan=2, colspan=3)
    ax[1].plot(X_Coordinates, beta_list, 'r.-')
    ax[1].plot(X_Coordinates, threshold_List, 'r--')
    ax[1].set_title('Peak Plot', )

    ax[2] = plt.subplot2grid((6,7), (0,4), rowspan=2, colspan=3)
    ax[2].plot(Smooth_X_Coordinates, Smooth_Y_Coordinates)
    ax[2].set_title('Smoothed graph')

    ax[3] = plt.subplot2grid((6,7), (3,4), rowspan=2, colspan=3)
    ax[3].plot(xnew, f(xnew))
    ax[3].set_title('Interpolated')
    
    ax[4] = plt.subplot2grid((6,7), (5,0), colspan=7)
    ax[4].set_position([0.25, 0.1, 0.65, 0.03])    
    thres = Slider(ax[4], 'Threshold', 0.000, 0.005, valinit = threshold, valfmt='%1.5f')        
    
    def update(val):
        threshold = thres.val
        print ("Threshold value: "), threshold
        smoothing_Plot(total_Span, threshold)
        fig.canvas.draw_idle()
    thres.on_changed(update)

    plt.show()



"""Main method to invoke other methods"""
def main():
    read_Input()
    window_Span = float(input("Please enter the window span"))
    construct_Alphalist(window_Span)
    construct_Betalist()
    total_Span  = 2*window_Span
    threshold   = float(input("Please enter the threshold value"))
    smoothing_Plot(total_Span, threshold)

main()
    