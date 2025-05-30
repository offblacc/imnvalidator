# strategies/test_big.py

from config import state
import util
import config
verbose = config.config.VERBOSE

async def test_big(test_config):
    output = ''
    status = None
    if "IMUNES warning - Issues encountered while creating nodes" in state.imunes_output:
        output += util.format_fail_test('Warnings while starting simulation')
        status = False
        if verbose:
            pass # if verbose then sim creation already printed the errors while creating
    else:
        output += util.format_pass_test('Simulation started without warnings')
        status = True
    
    return status, output
