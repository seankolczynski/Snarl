from enum import Enum, unique

@unique
class Status(Enum):
    NOGAME = -1
    INPROGRESS = 0
    INPROGRESSWON = 1
    LOST = 2
    WON = 3
