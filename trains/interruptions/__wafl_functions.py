from wafl.exceptions import CloseConversation, InterruptTask


async def close_conversation(inference, task_memory):
    raise CloseConversation


async def close_task(inference, task_memory):
    raise InterruptTask
