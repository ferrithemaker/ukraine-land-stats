import requests

# area function returns the area of a geojson polygon in square meters
from area import area

import credentials

import pymongo

# load credentials
user = credentials.login['user']
password = credentials.login['password']
url = credentials.login['url']

# connect to mongodb
client = pymongo.MongoClient("mongodb+srv://"+user+":"+password+"@"+url+"/?retryWrites=true&w=majority")
db = client.ukraine_land_stats
collection = db.land_data

# clean ALL previous data
collection.delete_many({})

# color codes
# #0f9d58 #0288d1 - Liberated
# #ff5252 #880e4f #a52714 #000000 - Occupied
# #bcaaa4 - Contested

# set false to ignore pre 2014 occupation and occupied territories not in ukraine
include_pre2022 = False
no_ukrainian_occupation = False

# historic data approx. every week from 3-4-22 to 29-12-22
timestamps = [1648989208, 1649616561, 1650217084, 1650820154, 1651432119, 1652037394, 1652649626
              , 1653244377, 1653860666, 1654444727, 1655069785, 1655669874, 1656248124, 1656868117
              , 1657393470, 1658009478, 1658687367, 1659264086, 1659891938, 1660513442, 1660417820
              , 1661030558, 1661718037, 1662300023, 1662907210, 1663537536, 1664141413, 1664736558
              , 1665351604, 1665871137, 1666561008, 1667169761, 1667687093, 1668296906, 1668984791
              , 1669587257, 1670191262, 1670798042, 1671404089, 1671922927, 1672269789]


for timestamp in timestamps:
    # old geojson data
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
            if feature["properties"]["fill"] == "#0f9d58" \
                    or feature["properties"]["fill"] == "#0288d1":
                polygonCount += 1
                status = "Liberated"
                liberated_m2 += areaOfPolygon
            if (feature["properties"]["fill"] == "#ff5252" and no_ukrainian_occupation) \
                    or (feature["properties"]["fill"] == "#880e4f" and include_pre2022) \
                    or (feature["properties"]["fill"] == "#000000" and include_pre2022) \
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
    liberated_percent = round((liberated_m2 / total_m2)*100, 2)
    occupied_percent = round((occupied_m2 / total_m2)*100, 2)
    contested_percent = round((contested_m2 / total_m2)*100, 2)
    register = {"timestamp": timestamp, "total_m2": total_m2, "liberated_m2": liberated_m2,
                "occupied_m2": occupied_m2, "contested_m2": contested_m2,
                "liberated_percent": liberated_percent, "occupied_percent": occupied_percent,
                "contested_percent": contested_percent}
    collection.insert_one(register)
