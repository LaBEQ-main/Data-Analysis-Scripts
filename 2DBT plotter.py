# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Authors - Frank Duffy, LaBEQ / Sardashti Research Group, Clemson University

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
SCRIPT INFORMATION AND INSTRUCTIONS
Frank Duffy
LaBEQ
2/23/2023

This script processes and plots a 2DBT data set.

-> To use this script, you must provide the file location by setting the 'file' variable to the correct location. 
-> Ensure that you seperate folders with // instead of \. 
-> You must also provide the number of ramp sequences contained in the file. 
-> One ramp is defined as a single max field to min field data range.

Once ran, the script will take your data and seperate all the individual ramp sequence data sets from the whole in a list. 
It will then create an array whose size is determined by the number of temperature steps/ramp. The average resistance values per temperature and magnetic field strength step will 
be stored there. Step sizes are calculated automatically. Following that, the 2D array is passed to imshow and plotted.

"""

file = "C:\\Users\\fduff\\OneDrive\\Documents\\Clemson University\\LabEQ\\Data Analysis\\2DBT testing\\2023_02_15_A064_6x20umBars_before_anneal\\033\\033_Data.txt"

# enter the excitation current for this experiment in units of Amps
excurr = 0.0001

maxfield = 8
minfield = -0.5

# enter the column names for the relevant data
voltage_column = "NF res"
temp_setpoint_column = "temp setpoint (K)"
temp_measured_column = "probe temp (K)"
field_measured_column = "field (T)"

df = pd.read_csv(file, sep = '\t')

# gather temperature step list
templist = df[temp_setpoint_column].unique()

print(templist)

#gather list of datasets at each temperature
ramp_data_list = []
for temp in templist:
    ramp_data_list.append(df[df[temp_setpoint_column] == temp])

print(len(ramp_data_list))
rampcount = len(ramp_data_list)

#test that the mean temperatures per ramp were roughly equivalent to the expected values.
for ramp_data in ramp_data_list:
    print(f"mean temp: " + str(ramp_data["probe temp (K)"].mean()) + ", datapoints: " + str(len(ramp_data)))
print(ramp_data_list[0])

#now lets ensure that all the individuated data is in ascending order with respect to field (T).
sorted_ramp_data_list =[]
for ramp_data in ramp_data_list:
    sorted_ramp_data_list.append(ramp_data.sort_values(by=[field_measured_column]))
print(sorted_ramp_data_list[0])

#np.zeroes returns an empty 2D array for us to store our averaged resistance values in and later plot.
res = np.zeros((rampcount, rampcount))

#calculate full range of ramp
ramprange = maxfield - minfield

#fieldstep is calculated so that the final 2D array is N x N, in this case 36x36
fieldstep = ramprange/rampcount

#iterate through ramp data, split, and compute the average resistance
for j in range(rampcount):
    for i in range(rampcount):
        mask = (sorted_ramp_data_list[j]["field (T)"] <= maxfield-i*fieldstep) & (sorted_ramp_data_list[j]["field (T)"] >= maxfield-fieldstep-i*fieldstep)
        subset = sorted_ramp_data_list[j][mask]

        #might as well correct the resistances here
        meanres = subset[voltage_column].mean()/excurr*np.log(2)
        res[i][j] = meanres

fig = plt.figure()
ax = plt.axes()
im = plt.imshow(res, extent=[1.5, 10.25, 0, 8])
plt.xlabel("T (K)")
plt.ylabel("B (T)")

#the next line ensures that the color bar height matches the plot but messes up the labels
cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
cbar = plt.colorbar(im, cax=cax)
cbar.set_label("$R_S$ ($\Omega$/$\u25a1$)")

plt.show()

print(res)