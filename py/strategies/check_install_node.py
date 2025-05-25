
import config
import pexpect
import util
from constants import AWAITS_PROMPT
import subshell

verbose = config.config.VERBOSE

# .*  for now accounts for ansi ~garbage~


async def check_install_node(test_config) -> bool:
    status, print_output = True, ''
    num_failed = 0
    commands = test_config["commands"]
    nodes = test_config["on_nodes"]
    eid = config.state.eid
    
    for node in nodes:
        nodesh = subshell.NodeSubshell(node)
        for cmd in commands:
            cmdoutput = nodesh.send(cmd)
            cmd_status = nodesh.last_cmd_status
            if cmd_status != '0':
                print_output += util.format_fail_subtest(f'Command {cmd} on {node} failed with non-zero exit: {cmd_status}')
                status = False
                num_failed += 1
                if verbose:
                    print_output += cmdoutput + '\n'
            else:
                print_output += util.format_pass_subtest(f'Command {cmd} on {node} returned status {cmd_status}')
                # if verbose:
                #     print_output += cmdoutput + '\r\n'

    total = len(commands) * len(nodes)
    print_output += util.format_end_status(f'{total-num_failed}/{total} successful checks', num_failed == 0)
    return status, print_output