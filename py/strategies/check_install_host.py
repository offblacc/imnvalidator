# strategies/ping.py

import config
import pexpect
import util

# .*  for now accounts for ansi ~garbage~
PROMPT = r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.* ?# ?"
verbose = config.config.VERBOSE

# TODO fix the issue.. this requires a simulation by code design, but.. yep..
async def check_install_host(test_config) -> bool:
    status, print_output = True, ''
    num_failed = 0
    commands = test_config["commands"]
    child = pexpect.spawn('/bin/bash', encoding="utf-8", timeout=10)
        
    for cmd in commands:
        # await first or nth consecutive prompt
        child.expect(PROMPT)
        
        # send the command from the config file
        child.sendline(cmd)
        child.expect(PROMPT)
        
        # fetch output from the command for verbose output
        if verbose:
            cmdoutput = '\n'.join(child.before.strip().split('\r\n')[1:-1]) # strip the command 
            # add to print output after processing the return status of the command
        
        # check status of the last ran command
        child.sendline("echo $?")
        child.expect(r"\d+\r?\n")
        cmd_status = child.match.group(0).strip()
        
        if cmd_status != '0':
            print_output += util.format_fail_subtest(f'Command {cmd} failed with non-zero exit: {cmd_status}')
            status = False
            num_failed += 1
            if verbose:
                print_output += cmdoutput + '\r\n'
        else:
            print_output += util.format_pass_subtest(f'Command {cmd} returned status {cmd_status}')
            # if verbose:
            #     print_output += cmdoutput + '\r\n'


    print_output += util.format_end_status(f'{len(commands)-num_failed}/{len(commands)} successful checks', num_failed == 0)
    return status, print_output