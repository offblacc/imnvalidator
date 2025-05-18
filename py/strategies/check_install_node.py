
import config
import pexpect
import util
from constants import AWAITS_PROMPT

verbose = config.config.VERBOSE

# .*  for now accounts for ansi ~garbage~


async def check_install_node(test_config) -> bool:
    status, print_output = True, ''
    num_failed = 0
    commands = test_config["commands"]
    nodes = test_config["on_nodes"]
    eid = config.state.eid
    
    for node in nodes:
        child = pexpect.spawn(f'himage {node}@{eid}')
        
        for cmd in commands:
            child.expect(AWAITS_PROMPT)
            
            # send the command from the config file
            child.sendline(cmd)
            child.expect(AWAITS_PROMPT)
            
            # fetch output from the command for verbose output
            if verbose:
                cmdoutput = '\n'.join(child.before.strip().decode().split('\r\n')[1:-1]) # strip the command 
                # add to print output after processing the return status of the command
            
            # check status of the last ran command
            child.sendline("echo $?")
            child.expect(r"\d+\r?\n")
            cmd_status = child.match.group(0).decode().strip()
            
            if cmd_status != '0':
                print_output += util.format_fail_subtest(f'Command {cmd} on {node} failed with non-zero exit: {cmd_status}')
                status = False
                num_failed += 1
                if verbose:
                    print_output += cmdoutput + '\r\n'
            else:
                print_output += util.format_pass_subtest(f'Command {cmd} on {node} returned status {cmd_status}')
                # if verbose:
                #     print_output += cmdoutput + '\r\n'

    total = len(commands) * len(nodes)
    print_output += util.format_end_status(f'{total-num_failed}/{total} successful checks', num_failed == 0)
    return status, print_output