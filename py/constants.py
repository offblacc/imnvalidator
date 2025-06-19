from enum import Enum

class OS(Enum):
    LINUX = 1
    FREEBSD = 2

# should cover linux and freebsd variations
AWAITS_PROMPT = r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.* ?# ?"
AWAITS_FREEBSD_ROOT_PROMPT = r'# '
GENERIC_PROMPT = r'PEXPECT_PROMPT# '