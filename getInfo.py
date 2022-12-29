import requests
import geojson

r = requests.get('https://deepStatemap.live/api/history/last.geojson')
deepStateMapJson = r.json()
print(deepStateMapJson)
