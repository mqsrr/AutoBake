from enum import Enum


class OrderState(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    DONE = "Done"
