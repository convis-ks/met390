# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 2026
PURPOSE: Skew-T Plot
Station: Buffalo (KBUF), NY | 12/23/23
@author: Kristopher
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
 
col_names = ['pressure', 'height', 'temperature', 'dewpoint',
             'relh', 'mixr', 'direction', 'speed',
             'thta', 'thte', 'thtv']

#plot data 
df = pd.read_csv(r"C:/Users/krist/Downloads/Observations 12Z 12-23-22.txt", \
                 skiprows=8, sep=r'\s+',
                 names=col_names, na_values=['', ' '])
 
for col in ['pressure', 'temperature', 'dewpoint', 'direction', 'speed']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
 
df = df.dropna(subset=['pressure', 'temperature', 'dewpoint',
                       'direction', 'speed']).reset_index(drop=True)
 
p          = df['pressure'].values  * units.hPa
T          = df['temperature'].values * units.degC
Td         = df['dewpoint'].values  * units.degC
wind_speed = df['speed'].values     * units('m/s')
wind_dir   = df['direction'].values * units.degrees
u, v       = mpcalc.wind_components(wind_speed, wind_dir)
 
skew = SkewT()
 
skew.plot(p, T,  'r')
skew.plot(p, Td, 'g')
 
# Set spacing interval -- every 50 hPa from 100 to 1000 hPa
my_interval = np.arange(100, 1000, 25) * units('hPa')
ix          = mpcalc.resample_nn_1d(p, my_interval)
skew.plot_barbs(p[ix], u[ix], v[ix])
 
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
 
skew.ax.set_xlabel('Temperature (°C)', fontweight='bold', fontsize=13)
skew.ax.set_xlim(-50, 40)
skew.ax.set_ylabel('Pressure (hPa)',   fontweight='bold', fontsize=13)
skew.ax.set_ylim(1000, 100)
skew.ax.grid(True)
 
plt.title("Buffalo (KBUF)  |  23 December 2023  12 UTC",
          fontweight='bold', fontsize=11)
 
plt.savefig('skewt_KBUF_20231223_12Z.png', dpi=300, bbox_inches='tight')
plt.show()