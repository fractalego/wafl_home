import json
import requests

from datetime import datetime

latitude = "51.5390"
longitude = "-0.1426"

secrets = json.load(open("secrets.json"))

result = requests.get(
    f"https://rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud/metoffice/production/v0/forecasts/point/daily?excludeParameterMetadata=false&includeLocationName=true&latitude={latitude}&longitude={longitude}",
    headers={
        "X-IBM-Client-Id": secrets["key"],
        "X-IBM-Client-Secret": secrets["secret"],
    },
)
data = result.json()
today = datetime.now().strftime("%Y-%m-%d")
# for item in data['features'][0]['properties']['timeSeries']:
#    if today in item['time']:
#        print(item['time'])

print(json.dumps(data, indent=2))
