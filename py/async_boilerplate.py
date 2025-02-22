import asyncio
from contextlib import suppress

async def run_interactive_process(command):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    """async def output_reader(stream, prefix="OUT:"):
        while True:
            line = await stream.readline()
            if not line:
                break
            print(f"{prefix} {line.decode().strip()}")
            # Add your conditional logic here
            if "Enter your choice:" in line.decode():
                process.stdin.write(b"2\n")  # Auto-respond to prompts

    async def input_writer():
        while True:
            await asyncio.sleep(0.1)  # Throttle input
            # Add your input generation logic here
            if some_condition:
                process.stdin.write(b"custom_command\n")

    async def monitor():
        await asyncio.gather(
            output_reader(process.stdout),
            output_reader(process.stderr, "ERR:"),
            input_writer()
        )

    # Run with timeout
    try:
        await asyncio.wait_for(monitor(), timeout=30)
    except asyncio.TimeoutError:
        print("Timeout reached")
    """
    # Cleanup
    with suppress(Exception):
        process.terminate()
        await process.wait()