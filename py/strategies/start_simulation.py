import config
import util
import re
from typing import Tuple
import subshell

async def start_simulation(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, util.format_fail_test('Encountered warnings while starting simulation')
    else:
        return True, "Simulation has already started... ignoring this call; check your tests order in the config file (or report bug)"
    
    config.state.sim_running = True # is also set in util.start_simulation(), free to delete this line
    
    return True, util.format_pass_test('Started.')
