import config
import util
import re
from typing import Tuple
import subshell

async def arpcheck(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, util.format_fail_test('Encountered warnings while starting simulation')
        
    status, print_output = False, ''
    nodes = test_config["source_nodes"]
    
    max_checks = 0
    ok_cnt = 0
    for node in nodes:
        max_checks += len(list(nodes.values())[0])
    
    ## GET ARP TABLE ##
    for node in nodes:
        nodesh = subshell.NodeSubshell(node)
        arp_raw = nodesh.send('arp -an')
        pattern = r'\(([^)]+)\)\s+at\s+([0-9a-fA-F:]{17})'
        matches = re.findall(pattern, arp_raw)
        arp_dict = dict()
        for ip, mac in matches:
            arp_dict[ip] = mac
        
        config_requested = list(nodes.values())[0] # will be one dict inside, always
        for ip in config_requested:
            if config_requested[ip] == arp_dict[ip]:
                ok_cnt += 1
                print_output += util.format_pass_subtest(f'{ip} at {arp_dict[ip]}')
            else:
                print_output += util.format_fail_subtest(f'{ip} at {arp_dict[ip]}, not at {config_requested[ip]}')
            

    status = ok_cnt == max_checks    
    print_output += util.format_end_status(f"{ok_cnt}/{max_checks} arp table checks successful", status)
    
    await util.stop_simulation()
    return status, print_output
