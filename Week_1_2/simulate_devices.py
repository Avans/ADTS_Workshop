import pandas as pd
import os
import subprocess
import sys
import datetime

date_arg = None
countries = []

if '--minDate' in sys.argv:
        date_arg = pd.to_datetime(sys.argv[sys.argv.index('--minDate') + 1], errors='ignore')

if '--countries' in sys.argv:
        countries = sys.argv[sys.argv.index('--countries') + 1].split(',')

print(countries)

df = pd.read_csv('./covid_19_clean_complete.csv')
df['Province/State'] = df['Province/State'].fillna('')

df['Name'] = df['Country/Region']# + '_' + df['Province/State']
df.loc[df['Province/State'] != '', 'Name'] = df['Country/Region'] + '_' + df['Province/State']
df['Name'] = df['Name'].str.replace('\'', '')
df['Name'] = df['Name'].str.replace(' ', '-')
df['Name'] = df['Name'].str[:36]

# Some data shuffling for events
df = df.groupby('Date', group_keys=False).apply(pd.DataFrame.sample, frac=1)

df['Date'] =  pd.to_datetime(df['Date'])

if isinstance(date_arg, datetime.datetime):
        df = df[df['Date'] >= date_arg]

if len(countries) > 0:
        df = df[df['Name'].isin(countries)]

def format_geo(val):
    val = int(val * 10000)
    if val >= 0:
        return '01' + '{0:0{1}x}'.format(val, 8)
    else:
        return '000' + '{0:0{1}x}'.format(val, 8)[1:]

df['Lat_hex'] = df['Lat'].apply(format_geo)
df['Long_hex'] = df['Long'].apply(format_geo)

df['Date_hex'] = df['Date'].apply(lambda x: '{0:0{1}x}'.format(int(x.strftime('%Y%m%d')), 8))

df['Confirmed_hex'] = df['Confirmed'].astype(int).apply(lambda x: '{0:0{1}x}'.format(x, 6))
df['Deaths_hex'] = df['Deaths'].astype(int).apply(lambda x: '{0:0{1}x}'.format(x, 6))
df['Recovered_hex'] = df['Recovered'].astype(int).apply(lambda x: '{0:0{1}x}'.format(x, 6))
df['Active_hex'] = df['Active'].astype(int).apply(lambda x: '{0:0{1}x}'.format(x, 6))

selection = df[['Name', 'Date_hex', 'Confirmed_hex', 'Deaths_hex', 'Recovered_hex', 'Active_hex', 'Lat_hex', 'Long_hex']]

counter = 0
for _, row in selection.iterrows():
    counter += 1
    device_id = row[0]
    value = ''.join(row[1:])
    result = subprocess.run(['ttnctl', 'devices', 'simulate', device_id, value], shell=True, stdout=subprocess.PIPE, encoding='ascii')
    print(result.stdout)
    print(f'Sent record {counter}/{selection.shape[0]}')