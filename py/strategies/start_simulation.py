import config
import util
import re
from typing import Tuple
import subshell

async def start_simulation(test_config) -> Tuple[bool, str]:
    no_warn = await util.start_simulation()
    if not no_warn:
        return False, 'Encountered warnings while starting simulation'
    
    config.state.sim_running = True # is also set in util.start_simulation(), free to delete this line
    
    return True, util.format_pass_subtest('Started.')
