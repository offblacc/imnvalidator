from util import start_process

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

    """Test ping - ping and check return command
    for each node in nodes ping each ip in target_ips
    report each one and return success if all succeed, else fail
    TODO maybe don't ping oneself if user wants to test ping all to all? maybe a switch to decide
    TODO just pass everything
    TODO add options to set timeout and -c (-W and -c)
    """


async def test_ping(eid, test_config) -> bool:
    total, failed = 0, 0
    for node in test_config["nodes"]:
        for ip in test_config["target_ips"]:
            process = await start_process(
                f'himage -nt {node}@{eid} sh -c "ping -W 2 -c 2 {ip} > dev/null; echo \$?"'
            )
            output = await process.stdout.read()
            if output.decode().strip().split("\n")[-1] != "0":
                print(f"[FAIL] Node '{node}' failed to ping '{ip}'")
                failed += 1
            elif verbose:
                print(f"[OK] Node '{node}' pinged '{ip}' successfully")

    total = len(test_config["nodes"]) * len(test_config["target_ips"])
    print('\n' + ('[OK] ' if failed == 0 else '[FAIL] ') + f"{total - failed}/{total} pings successfull")
    
    return failed == 0

    # TODO add printing out the exact pings failing!


def test_neigh(name, fail, success, nodes, expect):
    pass


def run_test(test, *args):
    return test(*args)
