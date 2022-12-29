import requests
import geojson
import json

# area function returns the area of a geojson polygon in square meters
from area import area

import pymongo
from datetime import datetime

# color codes
# #0f9d58 - Liberated
# #ff5252 #880e4f #a52714 - Occupied
# #bcaaa4 - Contested

# set false to ignore pre 2014 occupation and occupied territories not in ukraine
include_pre2022 = False
no_ukrainian_occupation = False

timestamp = 1669847043

url_last = "https://deepStatemap.live/api/history/last.geojson"
# old geojson to test
url = "https://deepstatemap.live/api/history/"+str(timestamp)+"/geojson"

r = requests.get(url)
deepStateMapJson = r.json()
polygonCount = 0
liberated_m2 = 0
contested_m2 = 0
occupied_m2 = 0

# print(json.dumps(deepStateMapJson, indent=4))
for feature in deepStateMapJson["features"]:
    if feature["type"] == "Feature" \
            and feature["geometry"]["type"] == "Polygon":
        '''
            and "karelia" not in feature["properties"]["name"].lower() \
            and "estonia" not in feature["properties"]["name"].lower() \
            and "latvia" not in feature["properties"]["name"].lower() \
            and "prussia" not in feature["properties"]["name"].lower() \
            and "pechorsky" not in feature["properties"]["name"].lower() \
            and "transnistria" not in feature["properties"]["name"].lower() \
            and "ichkeria" not in feature["properties"]["name"].lower() \
            and "tskhinvali" not in feature["properties"]["name"].lower() \
            and "tskhinval" not in feature["properties"]["name"].lower() \
            and "abkhazia" not in feature["properties"]["name"].lower():
        '''
        areaOfPolygon = area(feature["geometry"])
        # print("Area of Polygon",polygonCount,":",areaOfPolygon," ", end = "" )
        # use fill as grouping criteria
        status = ""
        if feature["properties"]["fill"] == "#0f9d58":
            polygonCount += 1
            status = "Liberated"
            liberated_m2 += areaOfPolygon
        if (feature["properties"]["fill"] == "#ff5252" and no_ukrainian_occupation) \
                or (feature["properties"]["fill"] == "#880e4f" and include_pre2022) \
                or feature["properties"]["fill"] == "#a52714":
            polygonCount += 1
            status = "Occupied"
            occupied_m2 += areaOfPolygon
        if feature["properties"]["fill"] == "#bcaaa4":
            polygonCount += 1
            status = "Contested"
            contested_m2 += areaOfPolygon
        # print(status)
# print(polygonCount)
total_m2 = liberated_m2 + occupied_m2 + contested_m2
print("date:", )
if include_pre2022:
    print("since the maximum occupation of Ukrainian territory (pre feb22) to", datetime.fromtimestamp(timestamp), ":")
else:
    print("since the maximum occupation of Ukrainian territory (beyond feb22) to", datetime.fromtimestamp(timestamp), ":")
print(round((liberated_m2 / total_m2)*100, 2), "% of land has been liberated")
print(round((occupied_m2 / total_m2)*100, 2), "% of land remains occupied")
print(round((contested_m2 / total_m2)*100, 2), "% of land is contested")
