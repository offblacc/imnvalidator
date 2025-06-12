import config
import pexpect
import util
import time
from constants import AWAITS_PROMPT
from typing import Tuple
import subshell

async def _services(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, util.format_fail_test('Encountered warnings while starting simulation')

    eid = config.state.eid
    status, print_output = True, ''
    fail_cnt = 0
    total_cnt = 0
    time.sleep(10) # wait for the services to start in the simulation itself
    
    
    # ========================= FTP =========================
    total_cnt += 1
    nodesh = subshell.NodeSubshell('FTP')
    command = f'netstat -an | grep LISTEN | grep -q "21"'
    nodesh.send(command)
    cmdstatus = nodesh.last_cmd_status == '0'
    if not cmdstatus:
        status = False
        print_output += util.format_fail_subtest("FTP error")
        fail_cnt += 1
    else:
        print_output += util.format_pass_subtest("FTP OK")
    
    # ========================= SSH =========================
    total_cnt += 1
    nodesh = subshell.NodeSubshell('SSH')
    command = f'netstat -an | grep LISTEN | grep -q "22"'
    nodesh.send(command)
    cmdstatus = nodesh.last_cmd_status == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("SSH error")
        fail_cnt += 1
    else:
        print_output += util.format_pass_subtest("SSH OK")
    
    # ========================= TELNET =========================
    total_cnt += 1
    nodesh = subshell.NodeSubshell('TELNET')
    command = f'netstat -an | grep LISTEN | grep -q "23"'
    nodesh.send(command)
    cmdstatus = nodesh.last_cmd_status == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("TELNET error")
        fail_cnt += 1
    else:
        print_output += util.format_pass_subtest("TELNET OK")
    
    print_output += util.format_end_status(f"{total_cnt-fail_cnt}/{total_cnt} services test successful", fail_cnt == 0)
    nodesh.close() # redundant
    await util.stop_simulation()
    return status, print_output
