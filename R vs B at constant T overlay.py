# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Authors - Frank Duffy, LaBEQ / Sardashti Research Group, Clemson University
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from scipy.signal import savgol_filter
import os

""" SUMMARY

This script takes voltage, temperature and magnetic field data and creates 
an overlay of sheet resistance R vs magnet field B for a series of constant 
temperature magnetic field sweeps through a superconducting sample. 

"""
##############################################################################
############## USER INPUT START ##############################################
##############################################################################

# in the event that you only wish to plot a subset of the temperature data list, 
# set gather_templist_from_data to false and populate the variable templist
# with the desired values.
gather_templist_from_data = True

# list the temperatures you would like removed from the plot if you 
# chose gather_templist_from_data = True.
temp_remove_list = [1.5, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75]

# the list of temperatures to plot if # chose gather_templist_from_data = False.
templist = [1.75, 2.0, 2.25, 2.5, 2.75, 3.0]

# enter the file which contains the data with two backslashes "\\" in place of "/" like below.
file = "C:\\Users\\fduff\\OneDrive\\Documents\\Clemson University\\LabEQ\\Data Analysis\\NCSU\\2022_11_11_NCSU_A093_A069_A081\\004\\004_Data.txt"

# enter the excitation current for this experiment
excurr = 0.0001

# enter the column names for the relevant data
voltage_column = "NF res"
temp_setpoint_column = "temp setpoint (K)"
temp_measured_column = "probe temp (K)"
field_measured_column = "field (T)"

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
    plt.plot(x, y * excurr * np.log(2), label = lbl)
    print(f"mean temp: " + str(ds[temp_measured_column].mean()) + ", datapoints: " + str(len(ds)))

plt.xlabel("B (T)", fontsize = 18)
plt.xticks(fontsize = 14)

plt.ylabel("R (Ω/□)", fontsize = 18)
plt.yticks(fontsize = 14)

plt.legend(loc='lower left')
plt.show()
plt.tight_layout()