# Reginal Hurricane Transmission tower line failure calculation and visualization
import RegionalHurricaneTL_failure_calculation
import time
import os
import sys


start_time = time.time()
resolution = 2  # wind profile resolution
if resolution == 1:
    hurricane_model = 'WindProfile_LatLon_R1km'
    v10_speed = 'all_speedV10_R1km'
    v10_angle = 'all_angleV10_R1km'
elif resolution == 2:
    hurricane_model = 'WindProfile_LatLon_R2km'
    v10_speed = 'all_speedV10_R2km'
    v10_angle = 'all_angleV10_R2km'
elif resolution == 4:
    hurricane_model = 'WindProfile_LatLon_R4km'
    v10_speed = 'all_speedV10_R4km'
    v10_angle = 'all_angleV10_R4km'
else:
    print(f'The input resolution is: {resolution} \n,'
          f'Currently support resolution to be [1km, 2km, 4km]')
    sys.exit()

outputfd = 'output_v5'
outputfn = 'TowerLinePreProcessing_R2km'
RH = RegionalHurricaneTL_failure_calculation.RegionalHurricaneTLFailureCal(outputfd,outputfn)
boundary = 'boundary'
powernetwork_model = 'Texas System Buses and Branches with Geographical information.xlsx'
# TLpreprocessing = 'TowerLinePreProcessing_v1_efficient_R1km'
TLFragility = 'Tower-lineFailureProbability.xlsx'
RH.towerline_preprocessing(hurricane_model, powernetwork_model)
# time_interval_all = [0.5,1.0,1.5,2.0,2.5,3.0]
time_interval_all = [3.0]
for time_interval in time_interval_all:
    if abs(time_interval - 0.5) < 1.0e-4:
        string_ts = 'Half'
    elif abs(time_interval - 1.0) < 1.0e-4:
        string_ts = 'One'
    elif abs(time_interval - 1.5) < 1.0e-4:
        string_ts = 'OneAndHalf'
    elif abs(time_interval - 2.0) < 1.0e-4:
        string_ts = 'Two'
    elif abs(time_interval - 2.5) < 1.0e-4:
        string_ts = 'TwoAndHalf'
    elif abs(time_interval - 3.0) < 1.0e-4:
        string_ts = 'Three'
    else:
        print('Error: the time_interval should be [0.5, 1.0, 1.5, 2.0, 2.5, 3.0] hours \n',
              f'------current input {time_interval} hours------', os.linesep)
        sys.exit()
    RH.line_failure_probability_calculation(TLFragility, v10_angle, v10_speed, time_interval)
    Linefailure = f'LineFailureProbability_at_{string_ts}hour'
    RH.transmission_line_failure_visu(Linefailure, time_interval, boundary)
    RH.creating_video(time_interval)
    RH.playing_video(time_interval)

print('-------------------------------------------------------------------')
print('------------------------- Project Summary -------------------------')
print('-------------------------------------------------------------------')
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>Input Files >>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print(f'----- User Specified Wind Profile Resolution {resolution} --------')
print(f'----- Wind Profile: {hurricane_model}.mat-------------------------')
print(f'------------------------- Wind Speed -----------------------------\n'
      f'{v10_speed}.mat')
print(f'------------------------- Wind Angle -----------------------------\n'
      f'{v10_angle}.mat')
print(f'------------------------- Power System Model----------------------\n'
      f' {powernetwork_model}')
print('>>>>>>>>>>>>>>>>>>>>>>>>>  Output Files >>>>>>>>>>>>>>>>>>>>>>>>>>>')
print(f'------------------------- Output Folder --------------------------\n'
      f'{outputfd}')
print(f'------------------------- Pre-Processing File --------------------\n'
      f'{outputfn}.json')
print(f'------------------------- Line Failure File -----------------------\n'
      f'{Linefailure}.json')
print(f'------------------------- Visualization File ----------------------\n'
      f'{string_ts}hour')
print(f'------------------------- Project Processing Time -----------------\n'
      f'Total Processing Time: {time.time() - start_time}sec')

# time. sleep(10) 


print('################################################################################################################')
print('###############################  Optimal operation of the impacted power system...  ############################')
print('################################################################################################################')


import os
import sys
import numpy as np
import pandas as pd
import datetime
import Hrcn_SCUC 
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'Library'), 'share')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import plotly.express as px

Alfa = input('Line outage probability treshold (choose a value from the set:{0.1,0.5,0.9}: ')
Alfa = float(Alfa)  

path1 = os.getcwd()
folder_name = 'Input_offline'
image_folder = 'Images_ps'
path = os.path.join(path1, folder_name)
os.makedirs(path, exist_ok=True)

path2 = os.path.join(path1, image_folder)
item_lsh = 'LoadShedding'+str(int(10*Alfa))+'.xlsx'
in_ps = os.path.join(path, item_lsh)

PH = Hrcn_SCUC.HurricaneSCUC('Result_ps',image_folder)

if Alfa == 0.1 or Alfa == 0.5 or Alfa == 0.9:
    print(f'Creating images in the {path2} folder! It may take a few minutes...')
    PH.vis_img(in_ps)
    
else:
    print('Alfa value is not in set! Please choose again.')    




