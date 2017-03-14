import pandas as pd
import numpy as np
import os
import re
import csv
import requests

pc_file = os.path.join(os.pardir,"data","validated_postcodes_uniq.csv")
pcdf = pd.read_csv(pc_file, header=None, names={'postalcode'})
pcdf = pcdf.fillna('')

pc_latlon_file = os.path.join(os.pardir,"data", "pc_latlon.csv")
pc_latlon_df = pd.read_csv(pc_latlon_file)
pc_latlon_df = pc_latlon_df.fillna('')

def onemap_geocode(postalcode):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    onemap_request = 'https://developers.onemap.sg/commonapi/search?searchVal=' + str(postalcode) + '&returnGeom=Y&getAddrDetails=N'
#     print(onemap_request)
    response = requests.get(onemap_request)
    response_json = response.json()

    try:
        lat = response_json['results'][0]['LATITUDE']
        lon = response_json['results'][0]['LONGITUDE']
    except IndexError:
        lat = ''
        lon = ''
    # print('response for ' + postalcode + ': ' + lat + ", " + lon)
    return lat + ', ' + lon

geocode_counter = 0

notyet_geocoded = pcdf[~pcdf['postalcode'].isin(pc_latlon_df['postalcode'])]

with open(pc_latlon_file, 'a', newline='') as outfile:
    writer = csv.writer(outfile)
    for postalcode in notyet_geocoded['postalcode']:
        latlon = onemap_geocode(postalcode)
        lat = latlon.split(',')[0]
        lon = latlon.split(',')[1]

        newrow = [postalcode, lat, lon]
        writer.writerow(newrow)
        geocode_counter += 1
        print('#' + str(geocode_counter) + ": " + str(newrow))
    print("All done!")