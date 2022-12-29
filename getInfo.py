import requests
import geojson
import json
from area import area

r = requests.get('https://deepStatemap.live/api/history/last.geojson')
deepStateMapJson = r.json()
polygonCount = 0
#print(json.dumps(deepStateMapJson, indent=4))
for feature in deepStateMapJson["features"]:
    if feature["type"] == "Feature" and feature["geometry"]["type"] == "Polygon":
        polygonCount += 1
        areaOfPolygon = area(feature["geometry"])
        print("Area of Polygon",polygonCount,":",areaOfPolygon)
        # Use fill as grouping criteria
        print(feature["properties"]["name"],feature["properties"]["fill"])
print(polygonCount)
