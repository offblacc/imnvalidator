# strategies/rip.py

from . import verbose
import util
import config

async def rip(test_config) -> bool:
    output = ''
    output += util.format_pass_subtest("RIP to be implemented!")
    return True, output + util.format_pass_test("RIP not yet implemented, pass")
