import config
import pexpect
import util
import time
from constants import AWAITS_PROMPT
from typing import Tuple
import subshell

async def _services(test_config) -> Tuple[bool, str]:
    eid = config.state.eid
    status, print_output = True, ''
    time.sleep(10) # wait for the services to start in the simulation itself
    
    
    # ========================= FTP =========================
    nodesh = subshell.NodeSubshell('FTP')
    command = f'netstat -an | grep LISTEN | grep -q "21"'
    nodesh.send(command)
    cmdstatus = nodesh.last_cmd_status == '0'
    if not cmdstatus:
        status = False
        print_output += util.format_fail_subtest("FTP error")
    else:
        print_output += util.format_pass_subtest("FTP OK")
    
    # ========================= SSH =========================
    nodesh = subshell.NodeSubshell('SSH')
    command = f'netstat -an | grep LISTEN | grep -q "22"'
    nodesh.send(command)
    cmdstatus = nodesh.last_cmd_status == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("SSH error")
    else:
        print_output += util.format_pass_subtest("SSH OK")
    
    # ========================= TELNET =========================
    nodesh = subshell.NodeSubshell('TELNET')
    command = f'netstat -an | grep LISTEN | grep -q "23"'
    nodesh.send(command)
    cmdstatus = nodesh.last_cmd_status == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("TELNET error")
    else:
        print_output += util.format_pass_subtest("TELNET OK")
        
    nodesh.close() # redundant
    return status, print_output
