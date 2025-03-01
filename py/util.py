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

def format_pass_subtest(s: str) -> None:
    return f'...{green_code}[OK]{reset_code} {s}\n'
    
def format_fail_subtest(s: str) -> None:
    return f'...{red_code}[FAIL]{reset_code} {s}\n'

def format_pass_test(s: str) -> None:
    return f'{green_code}[PASS]{reset_code} {s}'

def format_fail_test(s: str) -> None:
    return f'{red_code}[FAIL]{reset_code} {s}'

def format_end_status(s: str, status: bool) -> None:
    """Status True is success, False is failure.
    """
    return f'{green_code}[PASS]{reset_code} {s}\n' if status else f'{red_code}[FAIL]{reset_code} {s}\n'
    

# TODO if you optimise pings - multiple calls in the same shell process, implement it here
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
    ret_str += f'    \{border}\n'
    return ret_str