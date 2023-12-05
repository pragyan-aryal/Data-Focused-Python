import pandas as pd

add_df = pd.read_csv("Data/Indeed/location.tsv", sep="\t")

latitude = []
longitude = []
region = []
county = []
locality = []

for v in add_df["values"]:
    val = eval(v)
    latitude.append(val["latitude"])
    longitude.append(val["longitude"])
    region.append(val["region"])
    county.append(val["county"])
    locality.append(val["locality"])


add_df["latitude"] = latitude
add_df["longitude"] = longitude
add_df["region"] = region
add_df["county"] = county
add_df["locality"] = locality

add_df.to_csv("Data/Indeed/merged.tsv", sep="\t", index=False)

df = pd.read_parquet("Data/Indeed/clean_location.parquet")

region = []
for loc in df["Clean_location"]:
    z = add_df.loc[add_df["location"] == loc]
    if z.empty:
        region.append("NA")
    else:
        region.append(z["region"].to_string().split("    ")[1])

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

df["latitude"] = latitude
df["longitude"] = longitude
df["region"] = region
df["county"] = county
df["locality"] = locality


df.to_csv("Data/Indeed/merged_locations.tsv", sep="\t")
