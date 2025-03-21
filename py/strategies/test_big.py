from . import verbose
from config import state
import util

async def test_big(eid, test_config):
    output = ''
    status = None
    if "IMUNES warning - Issues encountered while creating nodes" in state.imunes_output:
        output += util.format_fail_test('Warnings while starting simulation')
        status = False
        if verbose:
            print("TODO add output here, maybe unnecessary, verbose already prints it out while starting experiment")
    else:
        output += util.format_pass_test('Simulation started without warnings')
        status = True
    
    return status, output
