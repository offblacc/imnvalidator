import util, asyncio


verbose = False



def set_verbose(v):
    global verbose
    verbose = v



def assign_operation(
    keyword: str,
) -> callable:  # TODO reflection; make smth like this a fallback
    if keyword == "ping":
        return test_ping
    elif keyword == "neighbour":
        return test_neigh




def test_neigh(name, fail, success, nodes, expect):
    pass


def run_test(test, *args):
    return test(*args)
