import sys, json, os
import strategies
import asyncio


async def start_process(cmd: str):
    return await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )


# TODO unused
def get_ip_from_node(scheme, node_name):
    with open(scheme, "r"):
        scheme = json.load(scheme)


# TODO if you optimise pings - multiple calls in the same shell process, implement it here
# TODO after implementing this function, use it in the ping test itself
async def ping_check(source_node_name, target_ip, eid, timeout=2, count=2):
    process = await start_process(
        f'himage -nt {source_node_name}@{eid} sh -c "ping -W {timeout} -c {count} {target_ip} > dev/null; echo \$?"'
    )
    output = await process.stdout.read()
    output = output.decode().strip()
    ping_status = output.split("\n")[-1].strip() == '0'
    ping_output = output[:output.rfind('\n')].strip()
    return ping_status, ping_output    