import config
import util
import re
from typing import Tuple
import subshell


async def send_command_host(test_config) -> Tuple[bool, str]:
    print_output = ''
    if not config.state.sim_running:
        if config.config.VERBOSE:
            print("Notice: running send_command_host but haven't started a simulation yet.")

    hostsh = subshell.HostSubshell()
    cmdout = hostsh.send(test_config["command"]) + '\n'
    status = hostsh.last_cmd_status == '0'

    print_output += cmdout
    print_output += util.format_end_status(f"Command returned {hostsh.last_cmd_status}", status)
    
    return status, cmdout
