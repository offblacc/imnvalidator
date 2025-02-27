#!/usr/bin/python3

import sys
import json
import os
import strategies
import asyncio
import util
import argparse
from strategies import set_verbose


def get_verbose():
    global verbose  # TODO is the keyword needed?
    return verbose


async def main(
    imn_file, config_file, verbose=False
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
    global_status = True
    for test in test_config["tests"]:
        operation = strategies.assign_operation(test["test"])
        print(f'\nRunning test {test["name"]}')
        if not await operation(eid, test):
            global_status = False
        print("------------------------------------")

    print()  # just a newline
    if not global_status:
        util.print_fail_test("Some tests failed")
    else:
        util.print_pass_test("All tests passed!")


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

    args = parser.parse_args()

    # Run the main function with parsed arguments
    asyncio.run(main(args.imn_file, args.config_file, args.verbose))
