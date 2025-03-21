# strategies/__init__.py
import config

verbose = False

# TODO DEPRECATED, remove after migrating verbose to config
def set_verbose(value):
    global verbose
    verbose = value
