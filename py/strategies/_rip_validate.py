# strategies/rip.py

# TODO add RIPng

import util
import time
import config

verbose = config.config.VERBOSE

sleep_shortest = 10
sleep_short = 30
sleep_long = 120

async def _rip_validate(test_config) -> bool:
    print_output = ''
    status = True
    
    source_node = test_config["source_node"]
    router_turnoff = test_config["router_turnoff"]
    router_checkriptable = test_config["router_checkriptable"]
    target_ip4_subnet = test_config["target_ip4_subnet"]
    expected_initial_next_hop4 = test_config["initial_next_hop4"]
    expected_post_turnoff_next_hop4 = test_config["post_turnoff_next_hop4"]
    # link-local ipv6 messing this up:
    # target_ip6_subnet = test_config["target_ip6_subnet"]
    # expected_initial_next_hop6 = test_config["initial_next_hop6"]   
    # expected_post_turnoff_next_hop6 = test_config["post_turnoff_next_hop6"]
    
    ip4 = test_config.get("target_ip4")
    ip6 = test_config.get("target_ip6")
    
    time.sleep(15) # TODO temporary value, change later, as well as the constants above
    # TODO sleep in smaller intervals (to a limit..) until RIP is set up..
    # await multiple times try in a loop..


    ### ====================== Test initial pings ======================    
    ## IPv4 initial ping
    rt = await util.get_rip_table(router_checkriptable)
    ping_status, ping_output = await util.ping_check(source_node, ip4, config.state.eid)
    if not ping_status:
        return False, "Didn't converge initially. Error with test config or didn't wait long enough at the start.\n" + ping_output + rt
    print_output += util.format_pass_subtest("Initial IPv4 ping goes through")
    
    
    ## IPv6 initial ping
    rt = await util.get_ripng_table(router_checkriptable)
    ping_status, ping_output = await util.ping_check(source_node, ip6, config.state.eid)
    if not ping_status:
        return False, "Didn't converge initially. Error with test config or didn't wait long enough at the start.\n" + ping_output + rt
    print_output += util.format_pass_subtest("Initial IPv6 ping goes through")
      
    
    
    ## Initial RIP(/ng) table checking
    # ====================== RIP (ipv4) check ======================
    rip_table = await util.get_rip_table(router_checkriptable)
    next_hop = util.parse_rip_table(rip_table)[target_ip4_subnet]["nexthop"]
    if next_hop == expected_initial_next_hop4:
        print_output += util.format_pass_subtest(f"Next RIP hop (IPv4) before turnoff is correct: {expected_initial_next_hop4}")
    else:
        print_output += util.format_fail_subtest(f"Next RIP hop (IPv4) before turnoff is invalid, expected {expected_initial_next_hop4} got {next_hop}")
        status = False
    
    if verbose:
        print_output += "RIP table before turnoff:\n" + rip_table + '\n'

    # ====================== RIPng (ipv6) check ======================
    rip_table = await util.get_ripng_table(router_checkriptable)
    # next_hop = util.parse_ripng_table(rip_table)[target_ip6_subnet]["nexthop"]
    # if next_hop == expected_initial_next_hop6:
    #     print_output += util.format_pass_subtest(f"Next RIPng hop before turnoff is correct: {expected_initial_next_hop6}")
    # else:
    #     print_output += util.format_fail_subtest(f"Next RIPng hop before turnoff is invalid, expected {expected_initial_next_hop6} got {next_hop}")
    #     status = False
    
    if verbose:
        print_output += "RIPng table before turnoff:\n" + rip_table + '\n'
    
    # ====================== Stop a router and wait for new routes to propagate ======================
    await util.stopNode(router_turnoff)
    time.sleep(230) # too much?, 190 was too little
        
    
    ### ====================== Test pings after router turnoff ======================    
    ## IPv4 post turnoff ping
    rt = await util.get_rip_table(router_checkriptable)
    ping_status, ping_output = await util.ping_check(source_node, ip4, config.state.eid)
    if not ping_status:
        return False, "Didn't find a new route, possible RIP error." + ping_output + rt
    print_output += util.format_pass_subtest("Post turnoff IPv4 ping goes through")
    
    
    ## IPv6 post turnoff ping
    rt = await util.get_ripng_table(router_checkriptable)
    ping_status, ping_output = await util.ping_check(source_node, ip6, config.state.eid)
    if not ping_status:
        return False, "Didn't find a new route, possible RIP error." + ping_output + rt
    print_output += util.format_pass_subtest("Post turnoff IPv6 ping goes through")


    ## Post router turnoff RIP(/ng) table checking
    # ====================== RIP (ipv4) check ======================
    rip_table = await util.get_rip_table(router_checkriptable)
    next_hop = util.parse_rip_table(rip_table)[target_ip4_subnet]["nexthop"]
    if next_hop == expected_post_turnoff_next_hop4:
        print_output += util.format_pass_subtest(f"Next RIP hop (IPv4) after turnoff is correct: {expected_post_turnoff_next_hop4}")
    else:
        print_output += util.format_fail_subtest(f"Next RIP hop (IPv4) after  turnoff is invalid, expected {expected_post_turnoff_next_hop4} got {next_hop}")
        status = False
    
    if verbose:
        print_output += "RIP table after turnoff:\n" + rip_table + '\n'
        
    # ====================== RIPng (ipv6) check ======================
    rip_table = await util.get_ripng_table(router_checkriptable)
    # next_hop = util.parse_ripng_table(rip_table)[target_ip6_subnet]["nexthop"]
    # if next_hop == expected_post_turnoff_next_hop6:
    #     print_output += util.format_pass_subtest(f"Next RIPng hop before turnoff is correct: {expected_post_turnoff_next_hop6}")
    # else:
    #     print_output += util.format_fail_subtest(f"Next RIPng hop before turnoff is invalid, expected {expected_post_turnoff_next_hop6} got {next_hop}")
    #     status = False
    
    if verbose:
        print_output += "RIPng table before turnoff:\n" + rip_table + '\n'
    
    return status, print_output.strip() + '\n'
