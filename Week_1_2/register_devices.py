import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import time
import numpy as np
import os
import json
import subprocess
import struct

df = pd.read_csv('./covid_19_clean_complete.csv')
df['Name'] = df['Country/Region']# + '_' + df['Province/State']
df.loc[df['Province/State'] != '', 'Name'] = df['Country/Region'] + '_' + df['Province/State']
df['Name'] = df['Name'].str.replace('\'', '')
df['Name'] = df['Name'].str.replace(' ', '-')
df['Name'] = df['Name'].str[:36]

df_locs = df.groupby(['Name', 'Lat', 'Long'])

counter = 0
for key, vals in df_locs:
    counter += 1
    name = key[0]
    
    result = subprocess.run(['ttnctl', 'devices', 'register', name], encoding='ascii', shell=True, stdout=subprocess.PIPE)
    result = subprocess.run(['ttnctl', 'devices', 'set', name, '--latitude', str(key[2]), '--longitude', str(key[3])]
            , encoding='ascii', shell=True, stdout=subprocess.PIPE)
    print(result.stdout)
    
    print(f'Registered {name}. Device {counter}/{len(df_locs)}')