import util


verbose = False
# TODO add directional ping, or make [a,b] only check a->b, maybe that's better? or add modifiers (LATER...)
# TODO are nodes node names or node IPs? figure out what's better


def set_verbose(v):
    global verbose
    verbose = v
    
def format_output_frame(s):
    """Format the output with borders and lines.
    Used mainly (probably) for returning the raw
    output from a command that failed the test.

    Args:
        s (str): The string to format.

    Returns:
        _type_: A sort of box frame is added to the output
    """
    ret_str = ""
    s = s.strip().split("\n")
    border = '=' * (max(len(line) for line in s) + 2)
    ret_str += f'    /{border}\n'
    for line in s:
        ret_str += f'   || {line}\n'
    ret_str += f'    \{border}'
    return ret_str


def assign_operation(
    keyword: str,
) -> callable:  # TODO reflection; make smth like this a fallback
    if keyword == "ping":
        return test_ping
    elif keyword == "neighbour":
        return test_neigh


# TODO here add awaiting at the end ?
async def test_ping(eid, test_config) -> bool:
    total, failed = 0, 0
    for node in test_config["nodes"]:
        for ip in test_config["target_ips"]:
            status, output = await util.ping_check(node, ip, eid)
            
            if status: # test success
                if verbose:
                    util.print_pass_subtest(f'Node \'{node}\' pinged \'{ip}\' successfully')
            
            else: # test failure
                util.print_fail_subtest(f'Node \'{node}\' failed to ping \'{ip}\'')
                failed += 1
                if verbose:
                    print(format_output_frame(output))


    total = len(test_config["nodes"]) * len(test_config["target_ips"])
    
    if failed == 0:
        util.print_pass_test(f'{total - failed}/{total} pings successfull')
    else:
        util.print_fail_test(f'{total - failed}/{total} pings successfull')
    
    return failed == 0

def test_neigh(name, fail, success, nodes, expect):
    pass


def run_test(test, *args):
    return test(*args)
