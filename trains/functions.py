import requests

from fuzzywuzzy import process

lines_dict = {
    "overground": "overground",
    "circle": "tube",
    "bakerloo": "tube",
    "northern": "tube",
    "jubilee": "tube",
    "victoria": "tube",
    "metropolitan": "tube",
    "dlr": "dlr",
}


def normalize_name(linename):
    extracted, score = process.extract(linename, lines_dict.keys(), limit=1)[0]
    if score < 60:
        f"% SAY I did not quite get the line name %"
        linename = {"% Which line do you want to check? %"}
        return {f"% normalize_name('{linename}') %"}

    return extracted


def check_tfl_line(linename):
    if linename not in lines_dict.keys():
        f"% SAY I cannot find a line named {linename} %"
        return False

    result = requests.get(
        f"https://api.tfl.gov.uk/Line/Mode/{lines_dict[linename]}/disruption"
    )

    data = result.json()
    for item in data:
        if linename in item["description"].lower():
            f"% SAY There is some disruption on the {linename} line. %"
            return

    f"% SAY The {linename} line is running normally %"
