# strategies/rip.py

from . import verbose
import util, asyncio

async def rip(eid, test_config) -> bool:
    output = ''
    output += util.format_pass_subtest("RIP to be implemented!")
    return True, output + util.format_pass_test("RIP not yet implemented, pass")
