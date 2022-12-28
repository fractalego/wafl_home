import logging
import json

from fuzzywuzzy import process

lines_dict = {
    "overground": "overground",
    "circle": "tube",
    "northern": "tube",
    "jubilee": "tube",
    "victoria": "tube",
    "dlr": "dlr",
}


def get_shopping_list_in_english(inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        return "Nothing"

    return ", ".join(shopping_list)


def add_shopping_list(item, inference, task_memory):
    if "shopping" in item.lower():
        return False

    if "add " in item.lower():
        item = item.lower().replace("add ", "")

    if not inference.get_inference_answer(f" the user adds something to a grocery list -> The user adds {item} to a list ", task_memory):
        if not inference.get_inference_answer(f" Do you really want to add {item}?", task_memory):
            return False

    shopping_list = json.load(open("shopping_list.json"))
    if " and " in item:
        items_to_add = item.split(" and ")
        shopping_list.extend(items_to_add)

    else:
        shopping_list.append(item)
        
    json.dump(shopping_list, open("shopping_list.json", "w"))
    inference.get_inference_answer(f" SAY {item} has been added to the shopping list", task_memory)

def remove_from_shopping_list(item, inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        "% SAY the shopping list is already empty.%"
        return False

    extracted, score = process.extract(item, shopping_list, limit=1)[0]
    if score < 60:
        inference.get_inference_answer(f" SAY I did not quite get the item to remove ", task_memory)
        return False

    if not inference.get_inference_answer(f" Do you want to remove {extracted} from the shopping list? ", task_memory):
        return False

    shopping_list.remove(extracted)
    json.dump(shopping_list, open("shopping_list.json", "w"))


def remove_first_item_from_shopping_list(inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        "% SAY the shopping list is already empty.%"
        return False

    shopping_list.pop(0)
    json.dump(shopping_list, open("shopping_list.json", "w"))


def remove_last_item_from_shopping_list(inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        "% SAY the shopping list is already empty.%"
        return False

    shopping_list.pop(-1)
    json.dump(shopping_list, open("shopping_list.json", "w"))

    

def reset_shopping_list(inference, task_memory):
    shopping_list = []
    json.dump(shopping_list, open("shopping_list.json", "w"))
