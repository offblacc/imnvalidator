import sys, json, os
import strategies
import asyncio
from typing import Tuple

green_code = '\033[92m'
red_code = '\033[91m'
reset_code = '\033[0m'

async def start_process(cmd: str):
    return await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

def print_pass_subtest(s: str) -> None:
    print(f'...{green_code}[OK]{reset_code} {s}')
    
def print_fail_subtest(s: str) -> None:
    print(f'...{red_code}[FAIL]{reset_code} {s}')

def print_pass_test(s: str) -> None:
    print(f'{green_code}[PASS]{reset_code} {s}')

def print_fail_test(s: str) -> None:
    print(f'{red_code}[FAIL]{reset_code} {s}')

# TODO if you optimise pings - multiple calls in the same shell process, implement it here
# TODO after implementing this function, use it in the ping test itself
async def ping_check(source_node_name, target_ip, eid, timeout=2, count=2) -> Tuple[bool, str]:
    """sssssstringgggggggggggg

    Args:
        source_node_name (str): _description_
        target_ip (str): _description_
        eid (str): _description_
        timeout (int, optional): _description_. Defaults to 2.
        count (int, optional): _description_. Defaults to 2.

    Returns:
        Tuple[bool, str]: _description_
    """
    process = await start_process(
        f'himage -nt {source_node_name}@{eid} sh -c "ping -W {timeout} -c {count} {target_ip}; echo \$?"'
    )
    output = await process.stdout.read()
    output = output.decode().strip()
    ping_status = output.split("\n")[-1].strip() == "0"
    ping_output = output[:output.rfind('\n')].strip()

    return ping_status, ping_output
