# strategies/test_big.py

from config import state
import util
import config
verbose = config.config.VERBOSE

async def test_big(test_config):
    if not config.state.sim_running:
        await util.start_simulation()
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
    
    if not status:
        output += 'Try manually running big_simulation_resolve tests to find the right value of nodecreate timeout'
    await util.stop_simulation()
    return status, output
