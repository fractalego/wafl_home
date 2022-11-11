import logging
import json
import requests

from datetime import datetime, timedelta
from fuzzywuzzy import process
from wafl.exceptions import CloseConversation, InterruptTask

lines_dict = {
    "overground": "overground",
    "circle": "tube",
    "northern": "tube",
    "jubilee": "tube",
    "victoria": "tube",
    "dlr": "dlr",
}


_logger = logging.getLogger(__file__)

shopping_list = json.load(open("shopping_list.json"))


def get_shopping_list_in_english():
    if not shopping_list:
        return "Nothing"

    return ", ".join(shopping_list)


def add_shopping_list(item):
    if "shopping" in item.lower():
        return False

    if not "% {item} can be part of a shopping list %":
        if not f"% Do you really want to add {item}?%":
            return False

    shopping_list = json.load(open("shopping_list.json"))
    shopping_list.append(item)
    json.dump(shopping_list, open("shopping_list.json", "w"))
    {f"% SAY {item} has been added to the shopping list%"}
    while {"% Do you want to add anything else  %"}:
        item = {"% What do you want to add?%"}
        shopping_list.append(item)
        json.dump(shopping_list, open("shopping_list.json", "w"))
        {f"% SAY {item} has been added to the shopping list%"}
        {"% ERASE MEMORY %"}


def remove_from_shopping_list(item):
    if not shopping_list:
        return False

    extracted, score = process.extract(item, shopping_list, limit=1)[0]
    if score < 60:
        {f"% SAY I did not quite get the item to remove %"}
        return

    if not {f"% Do you want to remove {extracted} from the shopping list? %"}:
        return False

    shopping_list.remove(extracted)
    json.dump(shopping_list, open("shopping_list.json", "w"))


def reset_shopping_list():
    global shopping_list
    shopping_list = []
    json.dump(shopping_list, open("shopping_list.json", "w"))


def get_time():
    now = datetime.now()
    return now.strftime("%H %M")


def get_date():
    now = datetime.now()
    return now.strftime("%A %d %B %Y")


def close_conversation():
    raise CloseConversation


def close_task():
    raise InterruptTask


def normalize_name(linename):
    extracted, score = process.extract(linename, lines_dict.keys(), limit=1)[0]
    print("EXTRACTED!", extracted, score)
    if score < 60:
        {f"% SAY I did not quite get the line name %"}
        linename = {"% Which line do you want to check? %"}
        return {f"% normalize_name('{linename}') %"}

    return extracted


def check_tfl_line(linename):

    if linename not in lines_dict.keys():
        {f"% SAY I cannot find a line named {linename} %"}
        return

    result = requests.get(
        f"https://api.tfl.gov.uk/Line/Mode/{lines_dict[linename]}/disruption"
    )

    data = result.json()
    for item in data:
        if linename in item["description"].lower():
            {f"% SAY There is some disruption on the {linename} line. %"}
            return

    {f"% SAY The {linename} line is running normally %"}

    

def check_today_weather():
    latitude = "51.5390"
    longitude = "-0.1426"
    today = datetime.now().strftime("%Y-%m-%d")
    check_weather_lat_long(latitude, longitude, today)

    
def check_tomorrow_weather():
    latitude = "51.5390"
    longitude = "-0.1426"
    today = datetime.now()
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    check_weather_lat_long(latitude, longitude, tomorrow)


def check_weather_lat_long(latitude, longitude, day):
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
        {"% SAY There is a connection error to the weather API. Please try later. %"}
        return


    for item in data["features"][0]["properties"]["timeSeries"]:
        if day in item["time"]:
            {f"% SAY The temperature should be between {int(item['dayLowerBoundMaxTemp'])} and {int(item['dayUpperBoundMaxTemp'])}. %"}
            if item["dayProbabilityOfPrecipitation"] != 0:
                {f"% SAY The probability of rain is {item['dayProbabilityOfPrecipitation']} percent. %"}

            if item["dayProbabilityOfSnow"] != 0:
                {f"% SAY The probability of snow is {item['dayProbabilityOfSnow']} percent. %"}
