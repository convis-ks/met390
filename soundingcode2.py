import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from metpy.calc import wind_components
from metpy.plots import SkewT
from metpy.units import units

# File path for the sounding data
filepath = "/home/starr/rawsounding"

# Read the sounding data, skipping headers and handling column names manually
col_names = ['pressure', 'height', 'temperature', 'dewpoint',
             'relative_humidity', 'mixing_ratio', 'direction', 'speed',
             'theta', 'theta_e', 'theta_v']

# Load the data, skipping the metadata lines (first 6 lines with '---')
df = pd.read_fwf(filepath, skiprows=6, names=col_names)

# Drop any rows with missing pressure, temperature, or dewpoint
df = df.dropna(subset=['pressure', 'temperature', 'dewpoint',
                       'direction', 'speed', 'height'], how='any').reset_index(drop=True)

# Convert data to proper units
p = df['pressure'].values * units.hPa
T = df['temperature'].values * units.degC
Td = df['dewpoint'].values * units.degC
u, v = wind_components(df['speed'].values * units.knots,
                       df['direction'].values * units.degrees)

# Skew-T Plot
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig)

# Plot temperature and dewpoint
skew.plot(p, T, 'r', linewidth=2, label='Temperature')
skew.plot(p, Td, 'g', linewidth=2, label='Dew Point')

# Wind barbs
skew.plot_barbs(p[::15], u[::15], v[::15])

# Axis settings
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)

skew.ax.set_yticks([1000, 900, 800, 700, 600, 500,
                    400, 300, 200, 100])
skew.ax.set_xticks([-40, -30, -20, -10, 0, 10, 20, 30, 40])

skew.ax.xaxis.set_tick_params(labelsize=16, direction='out')
skew.ax.yaxis.set_tick_params(labelsize=16, direction='out')
skew.ax.set_ylabel('Pressure (hPa)', fontsize=24, fontweight='bold')
skew.ax.set_xlabel('Temperature (°C)', fontsize=24, fontweight='bold')
skew.ax.set_title("SGF 22 May 22 2011 0000z", fontsize=26, fontweight='bold')

# Thermodynamic lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

# Show plot
plt.tight_layout()
plt.show()
