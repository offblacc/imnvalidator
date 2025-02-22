# TODO functional or OO approach?
# trying functional for now...

def assign_operation(keyword: str) -> callable:
    if keyword == "ping":
        return test_ping
    elif keyword == "neighbour":
        return test_neigh

def test_ping():
    print("Running ping test")

def test_neigh():
    pass

def run_test(test):
    return test()
