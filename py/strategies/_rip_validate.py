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
    
    ## Step 4:
    # Shut down a node
    
    ## Step 5:
    # sleep - let new state update
    
    ## Step 6:
    # Check new route found after step 5 node shutdown
    
    ## TESTING FUNCTION
    # time.sleep(5)
    # print(util.ping_check())
    # await util.stopNode('pc')
    # time.sleep(30)
    ## TESTING FUNCTION
       
    print_output = ''
    
    source_node = test_config["source_node"]
    router_turnoff = test_config["router_turnoff"]
    router_checkriptable = test_config["router_checkriptable"]
    
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
    time.sleep(5) # TODO temporary value, change later, as well as the constants above
    # sleep in smaller intervals (to a limit..) until RIP is set up..
    
    ### Step 2
    for addr in addrs:
        ping_status, ping_output = await util.ping_check(source_node, addr, config.state.eid)
        if not ping_status:
            return False, "Didn't converge. Error with test config.\n" + ping_output
    print_output += util.format_pass_subtest("Ping after waiting passed - RIP success")
    
    print_output += util.format_pass_test("RIP seems to work")
    
    ### Step 3
    # vtysh print if verbose
    
    childp = pexpect.spawn(f'himage {router_checkriptable}@{config.state.eid}')
    childp.expect(r'.*:/# ') # await prompt
    childp.sendline(f'vtysh -c "show ip rip"')
    childp.expect('(Codes: .*)(?=\\r\\n)') # da bude konzistentno stavi r ispred pa makni escape \
    print("RIP table is")
    o = childp.match.group(0).decode().strip()
    print(o)
    
    ## Step 4
    await util.stopNode(router_turnoff)
    time.sleep(400) # too much, but 190 was too little, figure out what's happpening
    print("Checking RIP table after a little nap, did it update?:")
    childp = pexpect.spawn(f'himage {router_checkriptable}@{config.state.eid}')
    childp.expect(r'.*:/# ') # await prompt
    childp.sendline(f'vtysh -c "show ip rip"')
    childp.expect('(Codes: .*)(?=\\r\\n)') # da bude konzistentno stavi r ispred pa makni escape \
    print("RIP table is")
    o = childp.match.group(0).decode().strip()
    print(o)
    # TODO to verify route changed, parse the part w net 10.0.4.0
    return True, print_output
