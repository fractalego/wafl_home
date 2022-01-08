import logging
import json

from datetime import datetime
from wafl.exceptions import CloseConversation, InterruptTask


_logger = logging.getLogger(__file__)


def get_time():
    now = datetime.now()
    return now.strftime("%H,%M")

def close_conversation():
    raise CloseConversation


def close_task():
    raise InterruptTask

def check_tfl_line(linename):
    pass
