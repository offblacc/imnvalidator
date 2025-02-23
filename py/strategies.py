from util import start_process


# TODO functional or OO approach?
# trying functional for now...


def assign_operation(keyword: str) -> callable:
    if keyword == "ping":
        return test_ping
    elif keyword == "neighbour":
        return test_neigh


async def test_ping(eid, name, fail, success, nodes, expect):
    print(f"{nodes}")
    process = await start_process(f'sudo himage {nodes[0]}@{eid} ping 127.0.0.1')
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        pl = line.decode().strip()
        print(pl if pl not in ["0", "1"] else "")

        if pl.startswith("Experiment ID ="):
            eid = pl.split()[-1]
        return_code = pl



def test_neigh(name, fail, success, nodes, expect):
    pass


def run_test(test, *args):
    return test(*args)
