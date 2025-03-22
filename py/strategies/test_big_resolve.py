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
## 1. Extract simulation creation logic to util.
# That way you can simply in the same way start a new sim.
# This includes changing sim creation to the new function in validate.py.
# 

## 2. 