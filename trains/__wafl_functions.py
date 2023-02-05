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


def normalize_name(linename, inference, task_memory):
    extracted, score = process.extract(linename, lines_dict.keys(), limit=1)[0]
    print("EXTRACTED!", extracted, score)
    if score < 60:
        inference.get_inference_answer(f" SAY I did not quite get the line name ", task_memory)
        linename = {inference.get_inference_answer(f" Which line do you want to check? ", task_memory)}
        return {inference.get_inference_answer(f" normalize_name('{linename}') ", task_memory)}

    return extracted


def check_tfl_line(linename, inference, task_memory):
    if linename not in lines_dict.keys():
        inference.get_inference_answer(f" SAY I cannot find a line named {linename} ", task_memory)
        return False

    result = requests.get(
        f"https://api.tfl.gov.uk/Line/Mode/{lines_dict[linename]}/disruption"
    )

    data = result.json()
    for item in data:
        if linename in item["description"].lower():
            inference.get_inference_answer(f" SAY There is some disruption on the {linename} line. ", task_memory)
            return False

    inference.get_inference_answer(f" SAY The {linename} line is running normally ", task_memory)
