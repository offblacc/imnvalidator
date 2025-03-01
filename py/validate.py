#!/usr/bin/python3

import sys
import json
import os
import strategies
import asyncio
import util
import argparse
from strategies import set_verbose
import time


def get_verbose():
    global verbose  # TODO is the keyword needed?
    return verbose


async def main(
    imn_file, config_file, verbose, parallel
):  # TODO verbose=False is redundant ?
    verbose = verbose
    strategies.set_verbose(verbose)
    test_config = None

    try:
        with open(config_file, "r") as json_file:
            test_config = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Config file '{config_file}' is not a valid JSON file.")
        sys.exit(1)

    # run the simulation
    cmd = f"imunes -b {imn_file}; echo $?"

    if verbose:
        print(f"Starting simulation with command: {cmd.split(';')[0]}")
    else:
        print("Starting simulation")

    process = await util.start_process(cmd)

    # "live stream" simulation creation output
    return_code, eid = None, None
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        pl = line.decode().strip()
        if pl not in ["0", "1"] and verbose:
            print(pl)

        if pl.startswith("Experiment ID ="):
            eid = pl.split()[-1]
        return_code = pl

    # check return code
    if return_code != "0":
        print("Simulation failed to start")
        sys.exit(1)  # TODO and cleanup?
    elif return_code == "0":
        print(f"Simulation started successfully.")

    # then go and run each operation...
    failures = 0
    if parallel:
        tasks = [run_single_test(eid, test) for test in test_config["tests"]]
        results = await asyncio.gather(*tasks)
        for test, (status, output) in zip(test_config["tests"], results):
            print(output)
            if status:
                continue
            failures += 1
    else:
        # Run tests sequentially
        for test in test_config["tests"]:
            status, output = await run_single_test(eid, test)
            print(output)
            if status:
                continue
            failures += 1

    print()  # just a newline
    print(
        util.format_end_status(
            f"{len(test_config['tests']) - failures}/{len(test_config['tests'])} tests successful",
            failures == 0,
        )
    )


async def run_single_test(eid, test):
    operation = strategies.assign_operation(test["test"])
    status, output = await operation(eid, test)
    return status, f'\nRunning test {test["name"]}\n' + output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a simulation with specified arguments."
    )
    parser.add_argument("imn_file", help="Path to the imunes scheme")
    parser.add_argument(
        "config_file", help="Path to the JSON config file defining the tests"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    parser.add_argument(
        "-p", "--parallel", action="store_true", help="Run tests in parallel"
    )
    parser.add_argument(
        "-t", "--timeit", action="store_true", help="Time the execution"
    )

    args = parser.parse_args()

    if args.timeit:
        start = time.time()
    # Run the main function with parsed arguments
    asyncio.run(main(args.imn_file, args.config_file, args.verbose, args.parallel))

    if args.timeit:
        end = time.time()
        print(f"Execution time: {end - start} seconds")
