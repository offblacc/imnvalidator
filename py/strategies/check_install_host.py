import config
import pexpect
import util
import subshell
from constants import OS
# TODO for freebsd host prompt - new entry in constants.py required ('# ' only)

verbose = config.config.VERBOSE

version_check_prefix = '' # will exist for freebsd
version_check_postfix = '' # will exist for linux

if config.config.is_OS_linux():
    version_check_postfix = ' --version'
elif config.config.is_OS_freebsd():
    version_check_prefix = 'command -v '
    

# TODO fix the issue.. this requires a simulation by code design, but.. yep..
async def check_install_host(test_config) -> bool:
    status, print_output = True, ''
    num_failed = 0
    commands = test_config["commands"]
    print("getplaftorm is")
    print(config.config.get_platform())
    hostsh = subshell.HostSubshell(host=config.config.get_platform())
        
    for cmd in commands:
        cmdoutput = hostsh.send(f'{version_check_prefix}{cmd}{version_check_postfix}')

        # check status of the last ran command
        cmd_status = hostsh.last_cmd_status
        
        if cmd_status != '0':
            print_output += util.format_fail_subtest(f'Command {cmd} failed with non-zero exit: {cmd_status}')
            status = False
            num_failed += 1
            if verbose:
                print_output += cmdoutput + '\r\n'
        else:
            print_output += util.format_pass_subtest(f'Command {cmd} returned status {cmd_status}')
            # if verbose:
            #     print_output += cmdoutput + '\r\n'


    print_output += util.format_end_status(f'{len(commands)-num_failed}/{len(commands)} successful checks', num_failed == 0)
    return status, print_output