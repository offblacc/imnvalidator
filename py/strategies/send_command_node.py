import config
import util
import re
from typing import Tuple
import subshell

async def send_command_node(test_config) -> Tuple[bool, str]:
    print_output = ''
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, util.format_fail_test('Encountered warnings while starting simulation')

    nodesh = subshell.NodeSubshell(test_config["node"])
    cmdout = nodesh.send(test_config["command"]) + '\n'
    status = nodesh.last_cmd_status == '0'

    print_output += cmdout
    print_output += util.format_end_status(f"Command returned {nodesh.last_cmd_status}", status)

    return status, print_output
