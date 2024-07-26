from enum import Enum


class OvenState(Enum):
    WAITING = 6
    READY_TO_START = 4
    COOKING = 7
    DONE = 5
