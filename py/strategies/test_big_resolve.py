# strategies/test_big_resolve.py

from . import verbose
from config import state
import util

async def test_big_resolve(eid, test_config):
    output = ''
    status = None
    if "IMUNES warning - Issues encountered while creating nodes" in state.imunes_output:
        output += util.format_fail_test('Warnings while starting simulation')
        status = False
        if verbose:
            print("TODO add output here, maybe unnecessary, verbose already prints it out while starting experiment")
    else:
        output += util.format_pass_test('Simulation started without warnings')
        status = True
    
    return status, output


### Steps to implement this
## 0: Migrate eid to config.state
# 0.0 eid in config.state
# 0.1 change all strategies signatures, import config and use eid from it

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
