# strategies/ping.py

import util, asyncio
import config
verbose = config.config.VERBOSE

async def ping(test_config) -> bool:
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, 'Encountered warnings while starting simulation'

    eid = config.state.eid
    total = len(test_config["source_nodes"]) * len(test_config["target_ips"])
    failed = 0
    print_output = ""

    tasks = [
        util.ping_check(node, ip, eid)
        for node in test_config["source_nodes"]
        for ip in test_config["target_ips"]
    ]

    ## The default ping expect status is that the ping succeeds, therefore default option is true (mind the dumb 'not in')
    expect_success = test_config.get("expect", "true").lower() not in ["fail", "failure", "0", "f", "false"]

    ### FIXME since using pexpect() this is useless, not running in parallel i mean, because of pexpect()
    results = await asyncio.gather(*tasks)

    for (node, ip), (ping_status, output) in zip(
        [
            (node, ip)
            for node in test_config["source_nodes"]
            for ip in test_config["target_ips"]
        ],
        results,
    ):
        pstr = (
            f"Node '{node}' pinged '{ip}' successfully"
            if ping_status
            else f"Node '{node}' failed to ping '{ip}'"
        )
        format = (
            util.format_pass_subtest
            if ping_status == expect_success
            else util.format_fail_subtest
        )
        print_output += format(pstr)

        # additional info to print in event of test failure
        if ping_status != expect_success:
            failed += 1
            if verbose:
                print_output += f'Expected {"successful ping" if expect_success else "ping failure"}, got:\n'
                print_output += util.format_output_frame(output)

    format = util.format_fail_test if failed != 0 else util.format_pass_test
    print_output += format(f"{total - failed}/{total} pings successful")
    await util.stop_simulation()
    return failed == 0, print_output
