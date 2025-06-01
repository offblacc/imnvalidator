import config
import util
import re
from typing import Tuple
import subshell

async def stop_simulation(test_config) -> Tuple[bool, str]:
    await util.stop_simulation()
    config.state.sim_running = False
    
    return True, util.format_pass_subtest('Simulation stopped.')
