# strategies/rip.py

from . import verbose
import util

async def _rip_validate(eid, test_config) -> bool:
    """Used in conjunction with A SPECIFIC scheme. Operates on a few
    assumptions. Finish this doc later.

    Args:
        eid (_type_): _description_
        test_config (_type_): _description_

    Returns:
        bool: _description_
    """
    ### Steps
    ## Step 1:
    # Ping from node 'pc' to '10.0.4.10' immediately at the start of the simulation
    
    ## Step 2:
    # sleep - let RIP propagate
    
    ## Step 3:
    # Ping from node 'pc' to '10.0.4.10' and expect success
    
    ## Step 4:
    # Print out (if verbose) vtysh show ip rip && ipv6 ripng
    
    ## Step 5:
    # Call a function from util (that you still have not written) to validate the RIP tables themselves
    # to validate the output (will see how viable it is to have expected output - or outputs...)
    # maybe util.validate_rip_table and util.validate_ripng_table, with some leeway, make it flexible
    
    ### Step 1
    print_output = ''
    # Source node and target ip should not be able to communicate at the start of the simulation,
    # and when RIP converges they should be able to ping themselves (gonna test oneway only);
    # router_turnoff is the name of the router node to be shut off during the simulation
    # after initial routes are set up to test that the RIP adjusts and finds an alternative
    # route successfully
    source_node, target_ip, router_turnoff = None, None, None
    
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
    
    for addr in addrs:
        ping_status, ping_output = await util.ping_check(test_config["source_node"], addr, eid)
        if ping_status:
            print("Expected ping to fail at start of simulation. Error with test config. Exiting...")
    
    output += util.format_pass_subtest("RIP to be implemented!")
    return True, output + util.format_pass_test("RIP not yet implemented, pass")
