## TODO add getting the RIP table here..

import logging
import config
import asyncio
from typing import Tuple
import pexpect
import json
import os

green_code = '\033[92m'
red_code = '\033[91m'
reset_code = '\033[0m'
logger = logging.getLogger("imnvalidator")
    
async def start_process(cmd: str):
    return await asyncio.create_subprocess_shell(
        cmd,
        limit=1024 * 256, # 256 KiB buffer, imunes sometimes gives a long output # TODO might be unnecessary
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

async def ping_check(source_node_name, target_ip, eid, timeout=2, count=2) -> Tuple[bool, str]:
    command = f"himage {source_node_name}@{config.state.eid}"
    
    # Start interactive shell session with `himage`
    child = pexpect.spawn(command, encoding="utf-8", timeout=timeout + 10)

    # Ensure the shell is ready (wait for prompt)
    child.expect(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+:/# ')

    # Send the ping command
    child.sendline(f"ping -W {timeout} -c {count} {target_ip}")

    child.expect(r'(PING|ping) .+')  # Expect the PING line
    ping_output = child.before.strip()  # Capture everything before the match

    child.expect(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+:/# ')  # Wait for the shell prompt
    ping_output += "\n" + child.before.strip()  # Append the ping output
    
    # Extract ping output (excluding the prompt itself)
    ping_output = child.before.strip()

    # Send command to get the exit status ($?)
    child.sendline("echo $?")

    # Expect a number (exit code) followed by a newline, then wait for the next prompt
    # TTYs should end with \r\n, allow both just in case
    child.expect(r"\d+\r?\n")

    # Extract the exit status (last captured number)
    ping_status = child.match.group(0).strip() == '0'

    # Close the session
    child.sendline("exit")
    child.close()

    # Log result
    logger.debug(
        f"Pinging {target_ip} from {source_node_name}@{eid} with timeout={timeout}, count={count} "
        f"RETURNS status '{ping_status}' and output '{ping_output}'"
    )

    ping_output = ping_output[:ping_output.rfind('\n')].strip()
    return ping_status, ping_output


import json

def nodes_exist(imn_file, test_config_filepath) -> set:
    """Tests whether nodes from:
    'source_node',
    'source_nodes'

    fields in the json test config are in the IMUNES scheme themselves.
    Used to avoid stacktraces from deep within (...himage calls) saying
    node doesn't exist when connecting to it (and warn user of a, quite possibly, typo).

    When adding a new type of test TRY to have nodes the framework is connecting
    to in fields named source_node or source_nodes (or both, but why would you do that?). If
    for some reason there is need for a different name for a field in JSON that holds the
    nodes the framework is connecting to at one point, add them to this function in the
    appropriate list.

    It checks across all tests .. finish me

    Args:
        imn_file (_type_): _description_
        test_config_filepath (_type_): _description_

    Returns:
        set: A set of missing nodes.
    """

    chk_data_flds = [
        'source_node',
        'source_nodes',
        'on_nodes'
    ]

    with open(imn_file, 'r') as imn_f, open(test_config_filepath, 'r') as schema_f:
        imn_data = json.load(imn_f)
        test_data = json.load(schema_f)

        # Extract node names from IMN data
        imn_nodes = set(imn_data["nodes"][node]["name"] for node in imn_data["nodes"])

        # Collect nodes from test configuration
        test_config_nodes = set()

        for test in test_data["tests"]:
            for data_field in chk_data_flds:
                try:
                    n = test[data_field]
                    if isinstance(n, list):  # a list of nodes
                        test_config_nodes.update(n)
                    elif isinstance(n, str):  # a single node
                        test_config_nodes.add(n)
                    else:
                        raise ValueError('Unexpected node type')
                except KeyError:
                    pass

        missing = test_config_nodes - imn_nodes
        return missing


def read_JSON_from_file(JSON_filepath: str):
    with open(JSON_filepath, "r") as json_file:
        return json.load(json_file)

async def start_simulation():
    imn_file = config.config.imunes_filename
    print_live = config.config.VERBOSE
    config.state.imunes_output = '' # reset to empty for new sim output log
    
    cmd = f"imunes -b {imn_file}; echo $?"
    if config.config.VERBOSE:
        print(f"Starting simulation with command: {cmd.split(';')[0]}") # TODO not print ??
    else:
        print("Starting simulation") # TODO not print (..here)

    logger.debug(f'Starting simulation with command: {cmd.split(";")[0]}') # TODO not print ??

    process = await start_process(cmd)  # don't need a PTY here, just start the simulation & read output

    return_code = None
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        pl = line.decode().strip()
        
        if pl not in ["0", "1"]:
            config.state.imunes_output += pl + '\n'
            if print_live:
                print(pl)

        ## fetch and set eid
        if pl.startswith("Experiment ID ="):
            config.state.eid = pl.split()[-1]
        return_code = pl

    ## Check return code
    if return_code != "0":
        print("Simulation failed to start")
        logger.debug("Simulation failed to start")
        raise RuntimeError("Simulation failed to start")
    elif return_code == "0":
        print(f"Simulation started successfully.")
        logger.debug("Simulation started successfully.")

async def stop_simulation(eid=None) -> str:
    if not eid:
        eid = config.state.eid
    output = ''
    process = await start_process(f'sudo imunes -b -e {eid}')
    while True:
        line = await process.stdout.readline()
        if not line:
            eid = None # TODO makes no sense now that you've added stop_all_ran_sims()
            break
        output += line.decode().strip() + '\n'
    return output

async def stop_all_ran_sims():
    for eid in config.state.all_eids:
        stop_simulation(eid)

async def stopNode(node: str) -> bool:
    if config.config.is_OS_linux():
        ifaces = list()
        process = await start_process(f'himage {node}@{config.state.eid} ls -1 /sys/class/net')
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            ifaces.append(line.decode().strip())

        for ifc in ifaces:
            process = await start_process(f'himage {node}@{config.state.eid} ifconfig {ifc} down')
            line = ''
            while line:
                line = await process.stdout.readline() # await subprocess.. trickery again
    return True # TODO add return status, check if ifc down


async def _get_ripany_table(node: str, ripng: bool):
    childp = pexpect.spawn(f'himage {node}@{config.state.eid}')
    childp.expect(r'.*:/# ') # await prompt
    childp.sendline(f"vtysh -c \"show ip rip{'ng' if ripng else ''}\"")
    childp.expect('(Codes: .*)(?=\\r\\n)')
    ret = childp.match.group(0).decode().strip()
    return ret

async def get_rip_table(node: str):
    return await _get_ripany_table(node, False)

async def get_ripng_table(node: str):
    return await _get_ripany_table(node, True)


def parse_rip_table(raw_rip_table: str):
    ript = dict()
    raw_rip_table = raw_rip_table.replace("\\r\\n", "\n").split("\n")
    start = False
    for line in raw_rip_table:
        if not start:
            if line.strip().startswith("Network"):
                start = True
        elif start:
            line = line.split()[1:]
            ript.update(
                {
                    line[0]: {
                        "nexthop": line[1],
                        "metric": line[2],
                        "from": line[3],
                        "tag": line[4],
                        "time": line[5] if len(line) == 6 else None,
                    }
                }
            )

    return ript
    
    
def parse_ripng_table(raw_rip_table: str):
    start = False
    beg = True
    newentry = list()
    ript = dict()
    for line in raw_rip_table.replace('\\r\\n', '\n').split('\n'):
        if not start:
            if line.strip().startswith('Network'):
                start = True
        else:
            if beg:
                newentry.append(line.split()[1]) # "Network" column
                beg = False
            else:
                newentry.extend(line.split())
                ript.update(
                    {
                        newentry[0]: {
                            "nexthop": newentry[1],
                            "via": newentry[2],
                            "metric": newentry[3],
                            "tag": newentry[4],
                            "time": newentry[5] if len(newentry) == 6 else None,
                        }
                    }
                )
                # reset to build new entry
                beg = True
                newentry = list()
    return ript

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
