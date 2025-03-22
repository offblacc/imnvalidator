# strategies/rip.py

from . import verbose
import util
import time
import pexpect
import config


sleep_shortest = 10
sleep_short = 30
sleep_long = 120

async def _rip_validate(test_config) -> bool:
    """Used in conjunction with A SPECIFIC scheme. Operates on a few
    assumptions. Finish this doc later.

    Args:
        eid (int): Opis
        test_config (_type_): _description_

    Returns:
        bool: _description_
    """
    ## Step 1:
    # sleep - let RIP propagate
    
    ## Step 2:
    # Ping from node 'pc' to '10.0.4.10' and expect success
    
    ## Step 3:
    # Print out (if verbose) vtysh show ip rip && ipv6 ripng
       
    print_output = ''
    
    source_node, router_turnoff = None, None
    source_node = test_config["source_node"]
    router_turnoff = test_config["router_turnoff"]
    router_checkriptable = test_config["router_turnoff"]
    
    addrs = list()

    ip4 = test_config.get("target_ip4")
    ip6 = test_config.get("target_ip6")

    if ip4:
        addrs.append(ip4)
    if ip6:
        addrs.append(ip6)

    if not addrs:
        print("No target IPs to check. Error with test config. Exiting...")
        exit(1)
    
    ### Step 1
    time.sleep(15) # TODO temporary value, change later, as well as the constants above
    
    ### Step 2
    for addr in addrs:
        ping_status, ping_output = await util.ping_check(test_config["source_node"], addr, eid)
        if not ping_status:
            return False, "Didn't converge. Error with test config.\n" + ping_output
    print_output += util.format_pass_subtest("Ping after waiting passed - RIP success")
    
    print_output += util.format_pass_test("RIP seems to work")
    
    ### Step 3
    # vtysh print if verbose
    
    childp = pexpect.spawn(f'himage {router_checkriptable}@{eid}')
    
    childp.expect(r'.*:/# ') # await prompt
    
    childp.sendline(f'vtysh -c "show ip rip"')
    
    
    childp.expect('(Codes: .*)(?=\\r\\n)') # da bude konzistentno stavi r ispred pa makni escape \
    
    print("RIP table is")
    o = childp.match.group(0).decode().strip()
    print(o)
    
    # TODO shutdown a node and test it didn't break
        
    return True, print_output
