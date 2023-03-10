# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Authors - Frank Duffy, LaBEQ / Sardashti Research Group, Clemson University


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from scipy.signal import savgol_filter
import os

""" SUMMARY

This script takes voltage, temperature and magnetic field data and creates 
an overlay of sheet resistance R vs magnet field B for a series of constant 
temperature magnetic field sweeps through a superconducting sample. The mean
temperature at each temperature step is calculated and printed to the screen 
for comparison with the set points.

"""
##############################################################################
############## USER INPUT START ##############################################
##############################################################################

# gather_temp_list_from_data will create the list of temperature steps to plot
# automatically given your data set. Setting false allows you to select one or 
# more temp data to plot by populating templist with your desired temps.
gather_templist_from_data = True

# list the temperatures you would like removed from the plot if you 
# chose gather_templist_from_data = True. Outliers or bad data, etc.
temp_remove_list = []

# the list of temperatures to plot if # chose gather_templist_from_data = False.
templist = [1.75, 2.0, 2.25, 2.5, 2.75, 3.0]

# enter the file which contains the data with two backslashes "\\" in place of "/" like below.
file = "C:\\Users\\fduff\\OneDrive\\Documents\\Clemson University\\LabEQ\\Data Analysis\\2DBT testing\\2023_02_15_A064_6x20umBars_before_anneal\\033\\033_Data.txt"

# enter the excitation current for this experiment in units of Amps
excurr = 0.0001

# enter the column names for the relevant data
voltage_column = "NF res"
temp_setpoint_column = "temp setpoint (K)"
temp_measured_column = "probe temp (K)"
field_measured_column = "field (T)"

# resistance conversion factor
conversion = 10**-9

# y axis label
y_label = "R (n??/???)"

# choose your graph title and field axis range
plt.title("A093 R vs B", fontsize = 20)
plt.xlim([-0.5,0.5])

# save and run using either >python plot.py or >py plot.py

##############################################################################
############## USER INPUT END ################################################
##############################################################################

df = pd.read_csv(file, sep = '\t')

# iterate through dataframe and remove the unwanted data
# then collect the desired temperature values
if gather_templist_from_data == True:
    for temp in temp_remove_list:
        df = df[(df[temp_setpoint_column] != temp)]

    templist = df[temp_setpoint_column].unique()


dslist = []
for temp in templist:
    ds = df[df[temp_setpoint_column] == temp]
    x = ds[field_measured_column]
    y = ds[voltage_column]
    lbl = str(temp)+"K"
    plt.plot(x, y * excurr * np.log(2) / conversion, label = lbl)
    print(f"mean temp: " + str(ds[temp_measured_column].mean()) + ", datapoints: " + str(len(ds)))

plt.xlabel("B (T)", fontsize = 18)
plt.xticks(fontsize = 14)

plt.ylabel(y_label, fontsize = 18)
plt.yticks(fontsize = 14)

plt.legend(loc='lower left')
plt.show()
plt.tight_layout()