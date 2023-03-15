import json

from fuzzywuzzy import process


async def get_shopping_list_in_english(inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        return "Nothing"

    return ", ".join(shopping_list)


async def add_shopping_list(item, inference, task_memory):
    if "shopping" in item.lower():
        return False

    if "add " in item.lower():
        item = item.lower().replace("add ", "")

    if not {
        await inference.get_inference_answer(f" The user adds {item} to a list :- the user adds something to a grocery list ", task_memory)
    }:
        if not {await inference.get_inference_answer(f" Do you really want to add {item}?", task_memory)}:
            return False

    shopping_list = json.load(open("shopping_list.json"))
    if " and " in item:
        items_to_add = item.split(" and ")
        shopping_list.extend(items_to_add)

    else:
        shopping_list.append(item)

    json.dump(shopping_list, open("shopping_list.json", "w"))
    await inference.get_inference_answer(f" SAY {item} has been added to the shopping list", task_memory)
    return True


async def remove_from_shopping_list(item, inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        await inference.get_inference_answer(f" SAY the shopping list is already empty.", task_memory)
        return False

    extracted, score = process.extract(item, shopping_list, limit=1)[0]
    if score < 60:
        await inference.get_inference_answer(f" SAY I did not quite get the item to remove ", task_memory)
        return False

    if not {await inference.get_inference_answer(f" Do you want to remove {extracted} from the shopping list? ", task_memory)}:
        return False

    shopping_list.remove(extracted)
    json.dump(shopping_list, open("shopping_list.json", "w"))
    return True


async def remove_first_item_from_shopping_list(inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        await inference.get_inference_answer(f" SAY the shopping list is already empty.", task_memory)
        return False

    shopping_list.pop(0)
    json.dump(shopping_list, open("shopping_list.json", "w"))
    return True


async def remove_last_item_from_shopping_list(inference, task_memory):
    shopping_list = json.load(open("shopping_list.json"))
    if not shopping_list:
        await inference.get_inference_answer(f" SAY the shopping list is already empty.", task_memory)
        return False

    shopping_list.pop(-1)
    json.dump(shopping_list, open("shopping_list.json", "w"))
    return True


async def reset_shopping_list(inference, task_memory):
    shopping_list = []
    json.dump(shopping_list, open("shopping_list.json", "w"))
    return True
