import config
import util
import re
from typing import Tuple
import subshell


# TODO some action is probably expected before checking arp table, if sim is started here..
async def send_command_node(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        raise RuntimeError(
            "To use sent command host, you need to manually start simulation using test name start_simulation before this test"
        )

    nodesh = subshell.NodeSubshell(test_config["node"])
    cmdout = nodesh.send(test_config["command"]) + '\n'
    status = nodesh.last_cmd_status == '0'

    cmdout += util.format_pass_subtest("Command returned 0") if status else util.format_fail_subtest(f"Command returned {nodesh.last_cmd_status}")
    
    return status, cmdout
