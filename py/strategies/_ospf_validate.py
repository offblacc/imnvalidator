import util
import time
import config
from typing import Tuple

verbose = config.config.VERBOSE

def _ospf_validate(test_config) -> Tuple[bool, str]:
    print_output = ''
    status = True
    eid = config.state.eid
    
    src_node = test_config["source_node"]
    target_ip4 = test_config["target_ip4"]
    target_ip4_subnet = test_config["target_ip4_subnet"]
    target_ip6 = test_config["target_ipv6"]
    disable_link_n1 = test_config["disable_link_n1"]
    disable_link_n2 = test_config["disable_link_n2"]
    router_checkospftable = test_config["router_checkospftable"]
    initial_nexthop4 = test_config["initial_nexthop4"]
    post_turnoff_next_hop4 = test_config["post_turnoff_next_hop4"]
    
    ### ====================== Initial sleep - OSPF setup ======================
    time.sleep(40)
    
    ### ====================== Test initial pings ======================
    ## IPv4 initial ping
    pst = True # sanity reasons, don't question it, it's alright
    for _ in range(20):
        pst, __ = util.ping_check(src_node, target_ip4, eid)
        if pst:
            break
    
    if not pst:
        return False, util.format_fail_test("Initial IPv4 ping failed")
    
    
    ## IPv6 initial ping
    pst = True # sanity reasons, don't question it, it's alright
    for _ in range(20):
        pst, __ = util.ping_check(src_node, target_ip6, eid)
        if pst:
            break
    
    if not pst:
        return False, util.format_fail_test("Initial IPv6 ping failed")
    
    print_output += util.format_pass_subtest("Initial pings succeeded")
    
    ### ====================== Print OSPF tables ======================
    print_output += 'IPv4 OSPF table:' + '\n'
    print_output += util.get_ospf_table(router_checkospftable) + '\n'
    
    print_output += 'IPv6 OSPF table:' + '\n'
    print_output += util.get_ipv6_ospf_table(router_checkospftable) + '\n'
    
    
    ### ====================== Disable link ======================
    
    util.set_BER(disable_link_n1, disable_link_n2, 1)
    
    ### ====================== Short sleep ======================
    sl1 = 10
    time.sleep(sl1)
    
    ### ====================== Print OSPF tables after disabling link ======================
    print_output += f"Routes after {sl1} seconds:\n"
    
    print_output += 'IPv4 OSPF table:' + '\n'
    print_output += util.get_ospf_table(router_checkospftable) + '\n'
    
    print_output += 'IPv6 OSPF table:' + '\n'
    print_output += util.get_ipv6_ospf_table(router_checkospftable) + '\n'
    
    
    ### ====================== Restore link ======================
    util.set_BER(disable_link_n1, disable_link_n2, 0)
    
    ### ====================== Sleep again ======================
    time.sleep(40)
    
    ### ====================== Ping checks after reinstating link ======================
    ## IPv4 initial ping
    pst = True # sanity reasons, don't question it, it's alright
    for _ in range(20):
        pst, __ = util.ping_check(src_node, target_ip4, eid)
        if pst:
            break
    
    if not pst:
        return False, util.format_fail_test("Post router restart IPv4 ping failed")
    
    
    ## IPv6 initial ping
    pst = True # sanity reasons, don't question it, it's alright
    for _ in range(20):
        pst, __ = util.ping_check(src_node, target_ip6, eid)
        if pst:
            break
    
    if not pst:
        return False, util.format_fail_test("Post router restart IPv6 ping failed")
    
    print_output += util.format_pass_subtest("Post router restart pings succeeded")
