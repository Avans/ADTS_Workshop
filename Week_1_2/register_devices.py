import pandas as pd
import os
import subprocess

df = pd.read_csv('./covid_19_clean_complete.csv')
df['Province/State'] = df['Province/State'].fillna('')
df['Name'] = df['Country/Region']
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
    result = subprocess.run(['ttnctl', 'devices', 'set', name, '--latitude', str(key[1]), '--longitude', str(key[2])]
            , encoding='ascii', shell=True, stdout=subprocess.PIPE)
    print(result.stdout)
    
    print(f'Registered {name}. Device {counter}/{len(df_locs)}')