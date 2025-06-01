import config
import util
import re
from typing import Tuple
import subshell

async def send_command_node(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, 'Encountered warnings while starting simulation'

    nodesh = subshell.NodeSubshell(test_config["node"])
    cmdout = nodesh.send(test_config["command"]) + '\n'
    status = nodesh.last_cmd_status == '0'

    cmdout += util.format_pass_subtest("Command returned 0") if status else util.format_fail_subtest(f"Command returned {nodesh.last_cmd_status}")
    
    return status, cmdout
