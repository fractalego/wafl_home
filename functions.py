import logging
import json
import requests

from datetime import datetime
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
    shopping_list.append(item)
    json.dump(shopping_list, open("shopping_list.json", "w"))


def reset_shopping_list():
    global shopping_list
    shopping_list = []
    json.dump(shopping_list, open("shopping_list.json", "w"))


def get_time():
    now = datetime.now()
    return now.strftime("%H,%M")


def close_conversation():
    raise CloseConversation


def close_task():
    raise InterruptTask


def normalize_name(linename):
    extracted, score = process.extract(linename, lines_dict.keys(), limit=1)[0]
    if score < 70:
        {f"% I did not quite get the line name %"}
        return False

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

