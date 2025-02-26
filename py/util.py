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
    
def get_ip_from_node(scheme, node_name):
    with open(scheme, 'r'):
        scheme = json.load(scheme)