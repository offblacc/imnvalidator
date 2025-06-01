import sys
import json
import asyncio
import util
import argparse
import util
import time
import logging
import importlib
import os
import config
import traceback

logger = logging.getLogger("imnvalidator")

async def main(imn_file, config_filepath, verbose, parallel, validate_install):
    config.config.VERBOSE = verbose
    config.config.validate_installation = validate_install
    
    if validate_install: # you got scheme and config pairs in tests/*/; get and set config variables, don't forget them
        await validate_installation()
        return
    else: # you got imn_file and config_filepath as args
        await validate_simulation(imn_file, config_filepath, verbose, parallel)
        return


async def validate_installation():
    # for each scheme.imn & test_config.json run validate_simulation(), then work out the quirks
    total_num_failed, names_failed = 0, []
    for dir in config.config.test_dir.iterdir():
        if not dir.is_dir():
            continue # we need subdirs
        if dir.name.startswith('.'):
            continue # ignore hidden (or ignored on purpose with . prepended)
        schemefile = dir / config.config.scheme_name
        configfile = dir / config.config.test_config_name
        if not os.path.isfile(schemefile) or not os.path.isfile(configfile):
            continue # check .imn and .json pair exists in the subdir
        
        ## ================= EXPLICITLY AVOID =================
        if dir.name == 'big_simulation_resolve':
            continue
        ## =====================================================
        
        print(f"Starting test {dir.name}")
        try:
            num_failed = await validate_simulation(schemefile, configfile, False, valinst=True)
            total_num_failed += num_failed
            if num_failed != 0:
                names_failed.append(dir.name)
        except Exception as e:
            names_failed.append(dir.name)
            total_num_failed += 1 # inconsistency with += num_failed above, but not that important
            print(f"Test {dir.name} ended with an exception:")
            print(e)
            print(f"Cleaning up after this sim and continuing with other tests")
            await util.stop_simulation()
        
            
    print(f"Number of failed tests: {total_num_failed}")
    if total_num_failed != 0:
        print(f"Tests failed: {', '.join(names_failed)}")

async def validate_simulation(imn_file, config_filepath, parallel, valinst=False):
    config.config.imunes_filename = imn_file
    config.config.test_config_filename = config_filepath    
    test_config = None


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
        print(
            "You have the following nodes specified in the test file that are not found in the IMUNES simulation:",
            ", ".join(missing),
        )
        exit(1)

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


    # if verbose: # don't print it.. clutter
    #     print(stop_output)


    if not valinst:
        print()  # just a newline
        print(
            util.format_end_status(
                f"{len(test_config['tests']) - failures}/{len(test_config['tests'])} tests successful",
                failures == 0,
            )
        )
    else:
        return failures


async def run_single_test(test):
    strategy_type = test["type"]
    strategy_module = importlib.import_module(f"strategies.{strategy_type}")
    strategy_function = getattr(strategy_module, strategy_type)

    status, output = await strategy_function(test)
    return status, f'\nRunning {test["name"]}\n' + output
    # return status, output



if __name__ == "__main__":
    log_to_file = True
    logger.debug("Program started")
    logger.debug("Parsing arguments")
    parser = argparse.ArgumentParser(
    description="Run framework with specified arguments."
)
    # Make these optional by setting nargs='?' and a default of None.
    parser.add_argument("imn_file", nargs="?", default=None, help="Path to the imunes scheme")
    parser.add_argument("config_file", nargs="?", default=None, help="Path to the JSON config file defining the tests")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-p", "--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("-t", "--timeit", action="store_true", help="Time the execution")
    parser.add_argument("-a", "--validate-installation", action="store_true",
                        help="Validate imunes installation itself running all in tests/")

    args = parser.parse_args()

    # Validate mutually exclusive modes:
    if args.validate_installation and (args.imn_file is not None or args.config_file is not None):
        parser.error("When using -a (--validate--installation), do not provide imn_file or config_file.")

    if not args.validate_installation and (args.imn_file is None or args.config_file is None):
        parser.error("Either provide both imn_file and config_file, or use --aggregate-run.")
    
    if args.timeit:
        start = time.time()

    logger.debug("Starting main function")
    
    
    try:
        failures = asyncio.run(
            main(
                args.imn_file,
                args.config_file,
                args.verbose,
                args.parallel,
                args.validate_installation,
            )
        )

    except Exception as e:
        print(traceback.format_exc())
        # print(f'Uncaught Exception: {e}')
        print(f'Stopping all started experiments')
        asyncio.run(util.stop_all_ran_sims())

    finally:
        asyncio.run(util.stop_all_ran_sims()) # redundant, let it stay here, zlu netrebalo
        if args.timeit:
            end = time.time()
            print(f"Execution time: {end - start} seconds")
            logger.info(f"Validator finished in {end - start} seconds")
