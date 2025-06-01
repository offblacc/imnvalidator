import config
import util
import re
from typing import Tuple
import subshell


async def send_command_host(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        if config.config.VERBOSE:
            print("Notice: running send_command_host but haven't started a simulation yet.")

    hostsh = subshell.HostSubshell()
    cmdout = hostsh.send(test_config["command"]) + '\n'
    status = hostsh.last_cmd_status == '0'

    cmdout += util.format_pass_subtest("Command returned 0") if status else util.format_fail_subtest(f"Command returned {nodesh.last_cmd_status}")
    
    return status, cmdout
