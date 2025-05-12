import config
import pexpect
import util
import time
from constants import AWAITS_PROMPT
from typing import Tuple


async def _services(test_config) -> Tuple[bool, str]:
    eid = config.state.eid
    status, print_output = True, ''
    child = pexpect.spawn('/bin/bash', encoding='utf-8')
    time.sleep(10) # wait for the services to start in the simulation itself
    
    # ========================= FTP =========================
    child.expect(AWAITS_PROMPT)
    command = f'himage FTP@{eid} netstat -an | grep LISTEN | grep -q "21"'
    child.sendline(command)
    child.expect(AWAITS_PROMPT)
    child.sendline("echo $?")
    child.expect(r"\d+\r?\n")
    cmdstatus = child.match.group(0).strip() == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("FTP error")
    else:
        print_output += util.format_pass_subtest("FTP OK")
    
    
    # ========================= SSH =========================
    child.expect(AWAITS_PROMPT)
    command = f'himage SSH@{eid} netstat -an | grep LISTEN | grep -q "22"'
    child.sendline(command)
    child.expect(AWAITS_PROMPT)
    child.sendline("echo $?")
    child.expect(r"\d+\r?\n")
    cmdstatus = child.match.group(0).strip() == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("SSH error")
    else:
        print_output += util.format_pass_subtest("SSH OK")
    
    
    # ========================= TELNET =========================
    child.expect(AWAITS_PROMPT)
    command = f'himage TELNET@{eid} netstat -an | grep LISTEN | grep -q "23"'
    child.sendline(command)
    child.expect(AWAITS_PROMPT)
    child.sendline("echo $?")
    child.expect(r"\d+\r?\n")
    cmdstatus = child.match.group(0).strip() == '0'
    if not cmdstatus: 
        status = False
        print_output += util.format_fail_subtest("TELNET error")
    else:
        print_output += util.format_pass_subtest("TELNET OK")
        
    return status, print_output
