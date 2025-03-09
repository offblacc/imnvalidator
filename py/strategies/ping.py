# strategies/ping.py

from . import verbose
import util, asyncio


async def ping(eid, test_config) -> bool:
    total = len(test_config["nodes"]) * len(test_config["target_ips"])
    failed = 0
    print_output = ""

    tasks = [
        util.ping_check(node, ip, eid)
        for node in test_config["nodes"]
        for ip in test_config["target_ips"]
    ]

    expect_success = test_config["expect"] not in ["fail", "failure", "0", "f", "false"]

    results = await asyncio.gather(*tasks)

    for (node, ip), (ping_status, output) in zip(
        [
            (node, ip)
            for node in test_config["nodes"]
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

        if ping_status != expect_success:
            failed += 1
            if verbose:
                print_output += util.format_output_frame(output)

    format = util.format_fail_test if failed != 0 else util.format_pass_test
    print_output += format(f"{total - failed}/{total} pings successful")
    return failed == 0, print_output
