# strategies/ping.py

from . import verbose
import util, asyncio
import config


async def check_install_node(test_config) -> bool:
    raise NotImplementedError