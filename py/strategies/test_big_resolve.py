# strategies/test_big_resolve.py

from . import verbose
import config
import util
import time

async def test_big_resolve(test_config):
    output = ''
    status = None
    
    process = await util.start_process("awk '/set nodecreate_timeout [0-9]+/ {print $3}'")
    current_timeout = await process.stdout.readline()
    
    if "IMUNES warning - Issues encountered while creating nodes" not in config.state.imunes_output:
        status = True
        output += util.format_pass_test(f'Simulation started without warnings with nodecreate_timeout = {current_timeout}')
        return status, output

    for tout in range(5, 100, 5):
        output += f'    trying with timeout value {tout}'
        util.stop_simulation()
        process = await util.start_process(f"sudo sed -i.bak 's/set nodecreate_timeout [0-9]\+/set nodecreate_timeout {tout}/' /usr/local/lib/imunes/imunes.tcl")
        time.sleep(2) # TODO replace with a function that uses pexpect to await next prompt after sending smth to stdin!!
        util.start_simulation()
        if "IMUNES warning - Issues encountered while creating nodes" not in config.state.imunes_output:
            status = True
            output += util.format_pass_test(f'Simulation started without warnings with nodecreate_timeout = {current_timeout}')
            return status, output
    
    return False, output
    
    
    
    
    ## Pazi - bit ćeš u ciklusu sa start - stop simulation, budi siguran da dobro rade te funkcije tamo

    # return status, output


### Steps to implement this
## 0: Migrate eid to config.state
# 0.0 eid in config.state +
# 0.1 change all strategies signatures, import config and use eid from it
# 0.2 REMOVE eid passing in validate.py @ run single test etc etc

## 1. Extract simulation creation logic to util.
# That way you can simply in the same way start a new sim.
# This includes changing sim creation to the new function in validate.py.
# Move eid variable also to config.py -> state
# Running the function should inherently change config.state.imunes_output
# the function should also inherently change config.state.eid

## 2. When warning, try bigger timeout
# sudo sed -i.bak 's/set nodecreate_timeout [0-9]\+/set nodecreate_timeout {new_timeout}/' /usr/local/lib/imunes/imunes.tcl
# you have to destroy the existing simulation (have eid here, but also config.state.eid; TODO MIGRATE this everywhere)
# then set new eid there
# you can extract the current number if needed with awk '/set nodecreate_timeout [0-9]+/ {print $3}' imunes.tcl

## POST - have a max value.. don't go to infinity


    return status, output