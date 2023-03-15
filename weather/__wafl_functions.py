import json
import requests

from datetime import datetime, timedelta

latitude = "51.4506"
longitude = "0.0571"


async def check_today_weather(inference, task_memory):
    today = datetime.now().strftime("%Y-%m-%d")
    await check_weather_lat_long(latitude, longitude, today, inference, task_memory)


async def check_tomorrow_weather(inference, task_memory):
    today = datetime.now()
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    await check_weather_lat_long(latitude, longitude, tomorrow, inference, task_memory)


async def check_weather_lat_long(latitude, longitude, day, inference, task_memory):
    secrets = json.load(open("secrets.json"))
    result = requests.get(
        f"https://rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud/metoffice/production/v0/forecasts/point/daily?excludeParameterMetadata=true&includeLocationName=true&latitude={latitude}&longitude={longitude}",
        headers={
            "X-IBM-Client-Id": secrets["key"],
            "X-IBM-Client-Secret": secrets["secret"],
        },
    )
    data = result.json()
    if "features" not in data:
        await inference.get_inference_answer(f" SAY There is a connection error to the weather API. Please try later. ", task_memory)
        return False

    for item in data["features"][0]["properties"]["timeSeries"]:
        if day in item["time"]:
            await inference.get_inference_answer(f" SAY The temperature should be between {int(item['dayLowerBoundMaxTemp'])} and {int(item['dayUpperBoundMaxTemp'])}. ", task_memory)
            if item["dayProbabilityOfPrecipitation"] != 0:
                await inference.get_inference_answer(f" SAY The probability of rain is {item['dayProbabilityOfPrecipitation']} percent. ", task_memory)

            if item["dayProbabilityOfSnow"] != 0:
                await inference.get_inference_answer(f" SAY The probability of snow is {item['dayProbabilityOfSnow']} percent. ", task_memory)
