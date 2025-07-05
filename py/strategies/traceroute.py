import util
import time
import config
from typing import Tuple

verbose = config.config.VERBOSE

async def traceroute(test_config) -> Tuple[bool, str]:
    if not config.state.sim_running:
        no_warn = await util.start_simulation()
        if not no_warn:
            return False, util.format_fail_test('Encountered warnings while starting simulation')

    status, print_output = True, ''
    pairs = test_config['src_tgt_pairs']
    total, failed = len(pairs), 0
    for src in pairs:
        if verbose:
            print_output += f'Testing traceroute from {src} to {pairs[src]}\n'
        trstatus = await util.trace_check(src, pairs[src])
        if trstatus:
            print_output += util.format_pass_subtest(f'{src} -> {pairs[src]} traceroute')
        else:
            status = False
            print_output += util.format_fail_subtest(f'{src} -> {pairs[src]} traceroute')
            failed += 1
    
    print_output += util.format_end_status(f"{total-failed}/{total} traceroutes successful", failed == 0)
    return status, print_output
