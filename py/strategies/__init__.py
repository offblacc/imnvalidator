# strategies/__init__.py
import config

verbose = config.config.VERBOSE

# TODO DEPRECATED, remove after migrating verbose to config
def set_verbose(value):
    global verbose
    verbose = value
