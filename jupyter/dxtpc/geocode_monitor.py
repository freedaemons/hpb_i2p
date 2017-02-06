import pandas as pd
import numpy as np
import os
import re
import requests
import matplotlib.pyplot as plt
%matplotlib inline 

pc_file = os.path.join(os.pardir,"data","postcodes_uniq.csv")
pcdf = pd.read_csv(pc_file, header=None, names={'postalcode'})
pcdf = pcdf.fillna('')
pcdf['lat'] = ''
pcdf['lon'] = ''
pcdf.to_csv(os.path.join(os.pardir,"data","pc_latlon.csv"), index=False)

pc_file = os.path.join(os.pardir,"data","pc_latlon.csv")
pcdf = pd.read_csv(pc_file)
pcdf = pcdf.fillna('')

validpc_regex = re.compile("\\b([0-9]{4}(?:[1-9][0-9]|[0-9][1-9]))")

pcdf['validity'] = pcdf['postalcode'].apply(lambda x: bool(re.search(validpc_regex, str(x))))

vpcdf = pcdf.loc[pcdf['validity'] == True][['postalcode', 'lat', 'lon']]
vpcdf = vpcdf.reset_index(drop=True)

def onemap_geocode(postalcode):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    onemap_request = 'https://developers.onemap.sg/commonapi/search?searchVal=' + postalcode + '&returnGeom=Y&getAddrDetails=N'
#     print(onemap_request)
    response = requests.get(onemap_request)
    response_json = response.json()

    try:
        lat = response_json['results'][0]['LATITUDE']
        lon = response_json['results'][0]['LONGITUDE']
    except IndexError:
        lat = ''
        lon = ''
    print('response for ' + postalcode + ': ' + lat + ", " + lon)
    return lat + ', ' + lon

vpcdf['latlon'] = vpcdf['postalcode'].apply(lambda x: onemap_geocode(x))

vpcdf['lat'] = vpcdf['latlon'].apply(lambda x: x.split(',')[0])
vpcdf['lon'] = vpcdf['latlon'].apply(lambda x: x.split(',')[1])

vpcdf = vpcdf[['postalcode', 'lat', 'lon']]
vpcdf.reset_index()

pc_latlon_file = os.path.join(os.pardir,"data","withlatlon.csv")
vpcdf.to_csv(pc_latlon_file)