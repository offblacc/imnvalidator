# strategies/test_big_resolve.py

import config
import util

TIMEOUT_MIN = 5
TIMEOUT_MAX = 100
TIMEOUT_STEP = 5
logger = config.config.logger
ERROR_MSG = "IMUNES warning - Issues encountered"

async def test_big_resolve(test_config):
    output = ''
    status = None
    
    logger.debug('Start of test_big_resolve: Fetching current nodecreate_timeout')
    process = await util.start_process("sudo awk '/set nodecreate_timeout [0-9]+/ {print $3}' /usr/local/lib/imunes/imunes.tcl")
    current_timeout = await process.stdout.readline()
    current_timeout = current_timeout.decode().strip()
    logger.debug(f'Got current nodecreate_timeout={current_timeout}')

    if ERROR_MSG not in config.state.imunes_output:
        status = True
        output += util.format_pass_test(f'Simulation started without warnings with nodecreate_timeout = {current_timeout}')
        logger.debug('Success in first try, no warnings from starting big sim')
        return status, output

    for tout in range(TIMEOUT_MIN, TIMEOUT_MAX, TIMEOUT_STEP):
        if int(current_timeout) > tout:
            logger.debug('current timeout is bigger than next one to try out; skipping iteration')
            continue # don't check values that obviously won't work, skip to first that might (> current) 
        
        output += f'    trying with timeout value {tout}\n'
        logger.debug('Got warnings, stopping simulation')
        print(f"Encountered warnings, changing nodecreate_timeout to {tout} and retrying")
        await util.stop_simulation()
        logger.debug('Simulation stopped')
        logger.debug(f'Changing timeout value to {tout}')
        ## Change value in imunes.tcl and double-check it was done
        command = ''
        # if config.config.is_OS_linux():
        command = f"sudo sed -i.bak \"s/set nodecreate_timeout [0-9]\\+/set nodecreate_timeout {tout}/\" /usr/local/lib/imunes/imunes.tcl; echo $?"
        process = await util.start_process(command)

        res = ''
        while True:
            l = await process.stdout.readline()
            res += l.decode().strip()
            if not l:
                break
        if res.strip() != '0':
            raise RuntimeError(f"Failed to modify imunes.tcl: {res}")
        
        process = await util.start_process("awk '/set nodecreate_timeout [0-9]+/ {print $3}' /usr/local/lib/imunes/imunes.tcl")
        checked_value = await process.stdout.readline()
        checked_value = checked_value.decode().strip()
        if checked_value != str(tout):
            raise RuntimeError(f"Failed to modify imunes.tcl, tried changing from {current_timeout} to {tout}, but after change it is {checked_value}")
        ## -
    
    
        logger.debug('Starting new simulation with changed eid')
        current_timeout = tout
        await util.start_simulation()
        logger.debug('Simulation started')
        if ERROR_MSG not in config.state.imunes_output:
            status = True
            output += util.format_pass_test(f'Simulation started without warnings with nodecreate_timeout = {current_timeout}')
            logger.debug(f'Got success with timeout={tout}')
            return status, output

    return False, output