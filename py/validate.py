#!/usr/bin/python3

import sys
import json
import asyncio
import util
import argparse
import util
import time
import logging
import importlib
import config
from helpers.schemavalidate import validateJSON

logger = logging.getLogger("imnvalidator")

schema_filepath = str(config.PROJECT_ROOT) + '/test_file_schema.json'

async def main(imn_file, config_filepath, verbose, parallel, validate_scheme) -> int:
    config.config.imunes_filename = imn_file
    config.config.test_config_filename = config_filepath
    config.config.set_verbose(verbose)

    test_config = None

    ## First, validate JSON file
    if not validate_scheme:
        json_valid, output = validateJSON(data_file_path=config_filepath, schema_file_path=schema_filepath)
        if not json_valid:
            print('Invalid JSON, reason:')
            print(output)
            exit(1)
        # TODO then check if you have tests that are not made to be run w other tests in the same file (that require restarting sim. etc; maybe later group them as a different type of tests?)e
    
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
        print('You have the following nodes specified in the test file that are not found in the IMUNES simulation:', ', '.join(missing))
        exit(1)

    await util.start_simulation()

    logger.debug(f'Running tests in {"parallel" if parallel else "sequence"}')
    
    ## Run each test
    failures = 0
    if parallel:
        # Run tests in parallel
        tasks = [run_single_test(test) for test in test_config["tests"]]
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
            status, output = await run_single_test(test)
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
        
    print('Cleaning up...')
    await util.stop_simulation()

    return failures

async def run_single_test(test):
    strategy_type = test["type"]
    strategy_module = importlib.import_module(f"strategies.{strategy_type}")
    strategy_function = getattr(strategy_module, strategy_type)

    status, output = await strategy_function(test)
    return status, f'\nRunning test {test["name"]}\n' + output


if __name__ == "__main__":
    log_to_file = True
    logger.debug("Program started")
    logger.debug("Parsing arguments")
    parser = argparse.ArgumentParser(
        description="Run framework with specified arguments."
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
    parser.add_argument(
        "-s", "--validate-scheme", action="store_true", help="Disable validating the test schema; useful during development"
    ) # remove this please TODO

    args = parser.parse_args()
    if args.timeit:
        start = time.time()

    logger.debug("Starting main function")
    failures = asyncio.run(main(args.imn_file, args.config_file, args.verbose, args.parallel, args.validate_scheme))

    if args.timeit:
        end = time.time()
        print(f"Execution time: {end - start} seconds")
        logger.info(f"Validator finished in {end - start} seconds")
    
    sys.exit(failures) # report the number of failed tests back to shell
