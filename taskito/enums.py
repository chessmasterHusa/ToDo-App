from enum import Enum

class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2

class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class MenuOption(Enum):
    EXIT = 0
    CREATE = 1
    UPDATE = 2
    SHOW = 3

class OSType(Enum):
    LINUX = 0
    WINDOWS = 1
