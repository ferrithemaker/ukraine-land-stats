import requests

# area function returns the area of a geojson polygon in square meters
from area import area

from datetime import datetime

# color codes
# #0f9d58 #0288d1 - Liberated
# #ff5252 #880e4f #a52714 #000000 - Occupied
# #bcaaa4 #bdbdbd - Contested

# set false to ignore pre 2014 occupation and occupied territories not in ukraine
include_pre2022 = False
no_ukrainian_occupation = False

timestamp = 1664141413
#timestamp = 1663537536

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
        areaOfPolygon = area(feature["geometry"])
        print("Area of Polygon",polygonCount,":",areaOfPolygon," ", end = "" )
        polygonCount += 1
        # use fill as grouping criteria
        status = ""
        if feature["properties"]["fill"] == "#0f9d58" \
                or feature["properties"]["fill"] == "#0288d1":
            status = "Liberated"
            liberated_m2 += areaOfPolygon
        if (feature["properties"]["fill"] == "#ff5252" and no_ukrainian_occupation) \
                or (feature["properties"]["fill"] == "#880e4f" and include_pre2022) \
                or (feature["properties"]["fill"] == "#000000" and include_pre2022) \
                or feature["properties"]["fill"] == "#a52714":
            status = "Occupied"
            occupied_m2 += areaOfPolygon
        if feature["properties"]["fill"] == "#bcaaa4" \
                or feature["properties"]["fill"] == "#bdbdbd":
            status = "Contested"
            contested_m2 += areaOfPolygon
        print(status,feature["properties"]["name"])
# print(polygonCount)
total_m2 = liberated_m2 + occupied_m2 + contested_m2
if include_pre2022:
    print(f"since the maximum occupation of Ukrainian territory (pre-feb22 occupied territories included) to {datetime.fromtimestamp(timestamp)}:")
else:
    print(f"since the maximum occupation of Ukrainian territory (pre-feb22 occupied territories NOT included) to {datetime.fromtimestamp(timestamp)}:")
print(f"{round((liberated_m2 / total_m2)*100, 2)} % of land has been liberated")
print(f"{round((occupied_m2 / total_m2)*100, 2)} % of land remains occupied")
print(f"{round((contested_m2 / total_m2)*100, 2)} % of land is contested")
print(f"{liberated_m2} m2 of land has been liberated")
print(f"{occupied_m2} m2 of land remains occupied")
print(f"{contested_m2} m2 of land is contested")
