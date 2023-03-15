from datetime import datetime, timedelta


async def get_date(inference, task_memory):
    now = datetime.now()
    return now.strftime("%A %d %B %Y")


async def get_time(inference, task_memory):
    now = datetime.now()
    minutes = int(now.strftime("%M"))
    hour = int(now.strftime("%H"))
    if minutes <= 30:
        return f"{minutes} past {hour}"

    else:
        return f"{60 - minutes} to {hour + 1}"
