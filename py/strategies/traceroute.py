import util
import time
import config
from typing import Tuple

verbose = config.config.VERBOSE

async def traceroute(test_config) -> Tuple[bool, str]:
    no_warn = await util.start_simulation()
    if not no_warn:
        return False, 'Encountered warnings while starting simulation'
    status, print_output = True, ''
    pairs = test_config['src_tgt_pairs']
    for src in pairs:
        if verbose:
            print_output += f'Testing traceroute from {src} to {pairs[src]}\n'
        trstatus = await util.trace_check(src, pairs[src])
        if trstatus:
            print_output += util.format_pass_subtest(f'{src} -> {pairs[src]} traceroute')
        else:
            status = False
            print_output += util.format_fail_subtest(f'{src} -> {pairs[src]} traceroute')
    await util.stop_simulation()
    return status, print_output
