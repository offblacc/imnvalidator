import logging
import strategies
import asyncio
from typing import Tuple
import pexpect
import sys

green_code = '\033[92m'
red_code = '\033[91m'
reset_code = '\033[0m'

global logger

def initialize_modules(verbose):
    global logger
    logger = logging.getLogger('imnvalidator')
    
    strategies.set_verbose(verbose)
    
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


def mprint(s: str) -> None:
    """Print to stdout using sys.stdout.write() and sys.stdout.flush()
    adding a newline at the end. Should be used instead of print() around
    pexpect to avoid buffering issues.

    Args:
        s (_str_): String to print to stdout.
    """
    sys.stdout.write(f'{s}\n')
    sys.stdout.flush()


async def ping_check(source_node_name, target_ip, eid, timeout=2, count=2) -> Tuple[bool, str]:
    command = f"himage {source_node_name}@{eid}"

    # Start interactive shell session with `himage`
    child = pexpect.spawn(command, encoding="utf-8", timeout=timeout + 2)

    # Ensure the shell is ready (wait for prompt)
    child.expect(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+:/# ')

    # Send the ping command
    child.sendline(f"ping -W {timeout} -c {count} {target_ip}")

    # Capture ping output until the next shell prompt appears
    child.expect(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+:/# ')

    # Extract ping output (excluding the prompt itself)
    ping_output = child.before.strip()
    mprint(f"ping output is {ping_output}")

    # Send command to get the exit status ($?)
    child.sendline("echo $?")

    # Expect a number (exit code) followed by a newline, then wait for the next prompt
    child.expect(r"\d+\r?\n")  # Match just the exit code output

    # Extract the exit status (last captured number)
    ping_status = child.match.group(0).strip()

    # Capture the exit status
    # child.expect(r'# ')
    # ping_status = child.before.strip()#.strip()# == "0"
    sys.stdout.flush()
    mprint(f"ping_status: {ping_status}")
    # Close the session
    child.sendline("exit")
    child.close()

    # Log result
    logger.debug(
        f"Pinging {target_ip} from {source_node_name}@{eid} with timeout={timeout}, count={count} "
        f"RETURNS status '{ping_status}' and output '{ping_output}'"
    )

    return ping_status, ping_output

# TODO if you optimise pings - multiple calls in the same shell process, implement it here
async def ping_check_old(source_node_name, target_ip, eid, timeout=2, count=2) -> Tuple[bool, str]:
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
    logger.debug(f'Pinging {target_ip} from {source_node_name}@{eid} with args timeout={timeout} and count={count} RETURNS status \'{ping_status}\' and output \'{ping_output}\' while the complete output was \'{output}\'')
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