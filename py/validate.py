#!/usr/bin/python3

import sys
import json
import asyncio
import util
import argparse
import util
import time
import logging
import strategies
import importlib
from helpers.schemavalidate import validateJSON

schema_filepath = 'test_file_schema.json'


def configure_logging(log_to_file=True, log_file="imnvalidator.log"):
    # Create a custom logger
    logger = logging.getLogger("imnvalidator")
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create handlers
    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    else:
        syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
        syslog_handler.setLevel(logging.DEBUG)
        logger.addHandler(syslog_handler)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    for handler in logger.handlers:
        handler.setFormatter(formatter)

    return logger

async def main(imn_file, config_filepath, verbose, parallel):
    global schema_filepath
    verbose = verbose
    test_config = None
    logger = logging.getLogger("imnvalidator")
    
    ## First, validate JSON file
    json_valid, output = validateJSON(data_file_path=config_filepath, schema_file_path=schema_filepath)
    if not json_valid:
        print('Invalid JSON, reason:')
        print(output)
        exit(1)
    else:
        if verbose:
            print('JSON file adheres to the schema.')
    
    ## Send verbose where it needs to go
    strategies.set_verbose(verbose)
    # util -> does it need verbose? shouldn't if you don't do anything wierd


    ## Try parsing the config file
    try:
        test_config = util.read_JSON_from_file(config_filepath)
    except FileNotFoundError:
        print(f"Error: Config file '{config_filepath}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Config file '{config_filepath}' is not a valid JSON file.")
        exit(1)
        
    
    ## Check nodes the framework will connect to even exist in the IMUNES file
    missing = util.nodes_exist(imn_file, config_filepath)
    if missing:
        print(f'You have the following nodes specified in the test file that are not found in the IMUNES simulation: {missing}')
        exit(1)
        
    ## Run the IMUNES simulation
    cmd = f"imunes -b {imn_file}; echo $?"
    if verbose:
        print(f"Starting simulation with command: {cmd.split(';')[0]}")
    else:
        print("Starting simulation")

    logger.debug(f'Starting simulation with command: {cmd.split(";")[0]}')

    process = await util.start_process(cmd)  # don't need a PTY here, just start the simulation & read output

    ## "live stream" simulation creation output line by line (if verbose)
    return_code, eid = None, None
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        pl = line.decode().strip()
        ## Print the line if verbose and not output of '; echo $?'
        if pl not in ["0", "1"] and verbose:
            print(pl)

        ## Fetch eid
        if pl.startswith("Experiment ID ="):
            eid = pl.split()[-1]
        return_code = pl

    ## Check return code
    if return_code != "0":
        print("Simulation failed to start")
        logger.debug("Simulation failed to start, exiting")
        sys.exit(1)
    elif return_code == "0":
        print(f"Simulation started successfully.")
        logger.debug("Simulation started successfully.")

    logger.debug(f'Running tests in {"parallel" if parallel else "sequence"}')
    
    ## Run each test
    failures = 0
    if parallel:
        # Run tests in parallel
        tasks = [run_single_test(eid, test) for test in test_config["tests"]]
        results = await asyncio.gather(*tasks)
        logger.debug("Tests finished")
        for test, (status, output) in zip(test_config["tests"], results):
            print(output)
            if status:
                logger.debug(f'Test {test["name"]} failed')
                continue
            else:
                logger.debug(f'Test {test["name"]} successful')
            failures += 1

        logger.debug(f"Tests finished with {failures} failures")
    else:
        # Run tests sequentially
        for test in test_config["tests"]:
            status, output = await run_single_test(eid, test)
            print(output)
            if status:
                logger.debug(f'Test {test["name"]} successful')
                continue
            else:
                logger.debug(f'Test {test["name"]} failed')
            failures += 1

        logger.debug(f"Tests finished with {failures} failures")

    print()  # just a newline
    print(
        util.format_end_status(
            f"{len(test_config['tests']) - failures}/{len(test_config['tests'])} tests successful",
            failures == 0,
        )
    )


async def run_single_test(eid, test):
    # operation = strategies.assign_operation(test['type']) # old way of doing it, keeping it here for old times sake
    strategy_type = test["type"]
    strategy_module = importlib.import_module(f"strategies.{strategy_type}")
    strategy_function = getattr(strategy_module, strategy_type)

    status, output = await strategy_function(eid, test)
    return status, f'\nRunning test {test["name"]}\n' + output


if __name__ == "__main__":
    log_to_file = True
    logger = configure_logging(log_to_file=log_to_file)
    logger.debug("Program started")
    logger.debug("Parsing arguments")
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
    logger.debug("Starting main function")
    asyncio.run(main(args.imn_file, args.config_file, args.verbose, args.parallel))

    if args.timeit:
        end = time.time()
        print(f"Execution time: {end - start} seconds")
        logger.info(f"Validator finished in {end - start} seconds")
