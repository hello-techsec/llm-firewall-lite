from enum import Enum

class Action(str, Enum):
    ALLOW = "ALLOW"
    REDACT = "REDACT"
    BLOCK = "BLOCK"
    LOG_ONLY = "LOG_ONLY"
