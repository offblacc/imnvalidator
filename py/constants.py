from enum import Enum
# constants.py

class OS(Enum):
    LINUX = 1
    FREEBSD = 2

# should cover linux and freebsd variations
AWAITS_PROMPT = r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.* ?# ?"
AWAITS_FREEBSD_ROOT_PROMPT = r'# '
