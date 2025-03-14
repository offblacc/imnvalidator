# strategies/ping.py

from . import verbose
import util, asyncio

async def rip(eid, test_config) -> bool:
    # before everything, check only rip is enabled, so it can be reliably tested
    # smisli najbolji način za dobivanje sheme ovdje
    # nešto što drži "stanje" - pamti sve te varijable neke bitne i ima gettere i settere
    # pa mu postaviš te neke varijable koje će ti trebati možda na raznim mjestima u kodu
    output = ''
    output += util.format_pass_subtest("RIP to be implemented!")
    return True, output + util.format_pass_test("RIP not yet implemented, pass")
