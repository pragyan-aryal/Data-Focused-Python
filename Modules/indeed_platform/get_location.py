import re
import pandas as pd
import time
import requests
import json
import numpy as np


def get_clean_location(sample="All"):

    print('\n Currently parsing the location and getting geo location for each job')

    df = pd.read_parquet('Final_Data/' + sample + '/' + 'merged.parquet')

    pat_1 = r"^Remote .*$"
    pat_2 = r"^Hybrid remote in.*$"

    loc = [line[10:] if re.search(pat_1, line) is not None else line[17:] if re.search(pat_2, line) is not None else line for line in df['Location']]

    df['Clean_location'] = [l.replace("\xa0", " ") for l in loc]

    pat_1 = r"^Remote .*$"
    pat_2 = r"^Hybrid remote in.*$"

    typ = ['Remote' if re.search(pat_1, line) is not None else 'Hybrid Remote' if re.search(pat_2, line) is not None else 'On-Site' for line in df['Location']]

    df['Work_Commute'] = typ

    df.to_parquet('Final_Data/' + sample + '/' + 'merged.parquet', index=False)

    unique_location = df['Clean_location'].unique()

    pat = r".*[Rr]emote.*$"

    locations = []
    for i in unique_location:
        if re.search(pat, i) is None:
            locations.append(i)

    with open('Final_Data/' + sample + '/loc.txt', 'w') as file:
        for i in locations:
            file.write(i + '\n')

    file.close()


def fetch_geo_loc(sample="All"):
    location_url = "http://api.positionstack.com/v1/forward?access_key=7beed071aee02b56a8cca2428cb9ec45&query={}"

    records = []

    with open('Final_Data/' + sample + '/loc.txt', 'r') as file:
        records = file.read().split('\n')

    address = {}

    for record in records:
        response = requests.get(location_url.format(record))
        r = json.loads(response.text)
        try:
            address[record] = r['data'][0]
        except:
            try:
                response = requests.get(location_url.format(record))
                r = json.loads(response.text)
                address[record] = r['data'][0]
            except:
                address[record] = 'NA'
        time.sleep(0.7)

    with open('Final_Data/' + sample + '/location.tsv', 'w') as file:
        file.write('location' + '\t' + 'values' + '\n')
        for a, v in address.items():
            file.write(a + '\t' + str(v) + '\n')


def merge_location(sample="All"):
    add_df = pd.read_csv("Final_Data/" + sample + "/location.tsv", sep="\t")

    latitude = []
    longitude = []
    region = []
    county = []
    locality = []
    country_code = []
    region_code = []

    for v in add_df["values"]:
        if str(v) != 'nan' and str(v) != 'NA':
            val = eval(v)
            latitude.append(val["latitude"])
            longitude.append(val["longitude"])
            region.append(val["region"])
            county.append(val["county"])
            locality.append(val["locality"])
            country_code.append(val['country_code'])
            region_code.append(val['region_code'])
        else:
            latitude.append(None)
            longitude.append(None)
            region.append(None)
            county.append(None)
            locality.append(None)
            country_code.append(None)
            region_code.append(None)

    add_df["latitude"] = latitude
    add_df["longitude"] = longitude
    add_df['region_code'] = region_code
    add_df["region"] = region
    add_df["county"] = county
    add_df["locality"] = locality
    add_df["country_code"] = country_code

    add_df.to_csv("Final_Data/" + sample + "/merged_location.tsv", sep="\t", index=False)

    df = pd.read_parquet("Final_Data/" + sample + "/" + "merged.parquet")

    region = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            region.append("NA")
        else:
            region.append(z["region"].to_string().split("    ")[1])

    region_code = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            region_code.append("NA")
        else:
            region_code.append(z["region_code"].to_string().split("    ")[1])

    locality = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            locality.append("NA")
        else:
            locality.append(z["locality"].to_string().split("    ")[1])

    county = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            county.append("NA")
        else:
            county.append(z["county"].to_string().split("    ")[1])

    latitude = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            latitude.append("NA")
        else:
            latitude.append(float(z["latitude"]))


    longitude = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            longitude.append("NA")
        else:
            longitude.append(float(z["longitude"]))

    country_code = []
    for loc in df["Clean_location"]:
        z = add_df.loc[add_df["location"] == loc]
        if z.empty:
            country_code.append("NA")
        else:
            country_code.append(z["country_code"].to_string().split("    ")[1])

    df["latitude"] = latitude
    df["longitude"] = longitude
    df['region_code'] = region_code
    df["region"] = region
    df["county"] = county
    df["locality"] = locality
    df["country_code"] = country_code

    df['latitude'].replace(['NA', ''], np.NaN, inplace=True)
    df['longitude'].replace(['NA', ''], np.NaN, inplace=True)
    df['region'].replace(['NA', ''], np.NaN, inplace=True)
    df['region_code'].replace(['NA', ''], np.NaN, inplace=True)
    df['county'].replace(['NA', ''], np.NaN, inplace=True)
    df['locality'].replace(['NA', ''], np.NaN, inplace=True)
    df['country_code'].replace(['NA', ''], np.NaN, inplace=True)
    df = df.drop(['Location'], axis=1)

    df.to_parquet("Final_Data/" + sample + "/merged.parquet", index=False)
