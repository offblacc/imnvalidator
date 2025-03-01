import util, asyncio


verbose = False
# TODO add directional ping, or make [a,b] only check a->b, maybe that's better? or add modifiers (LATER...)
# TODO are nodes node names or node IPs? figure out what's better


def set_verbose(v):
    global verbose
    verbose = v



def assign_operation(
    keyword: str,
) -> callable:  # TODO reflection; make smth like this a fallback
    if keyword == "ping":
        return test_ping
    elif keyword == "neighbour":
        return test_neigh


async def test_ping(eid, test_config) -> bool:
    total = len(test_config["nodes"]) * len(test_config["target_ips"])
    failed = 0
    print_output = ''

    tasks = [
        util.ping_check(node, ip, eid)
        for node in test_config["nodes"]
        for ip in test_config["target_ips"]
    ]

    results = await asyncio.gather(*tasks)

    for (node, ip), (status, output) in zip(
        [(node, ip) for node in test_config["nodes"] for ip in test_config["target_ips"]],
        results
    ):
        if status:
            if verbose:
                print_output += util.format_pass_subtest(f'Node \'{node}\' pinged \'{ip}\' successfully')
        else:
            print_output += util.format_fail_subtest(f'Node \'{node}\' failed to ping \'{ip}\'')
            failed += 1
            if verbose:
                print_output += util.format_output_frame(output)

    format = util.format_fail_test if failed != 0 else util.format_pass_test
    print_output += format(f'{total - failed}/{total} pings successful')
    return failed == 0, print_output

def test_neigh(name, fail, success, nodes, expect):
    pass


def run_test(test, *args):
    return test(*args)
