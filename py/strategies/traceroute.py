import util
import time
import config
from typing import Tuple

verbose = config.config.VERBOSE

async def traceroute(test_config) -> Tuple[bool, str]:
    