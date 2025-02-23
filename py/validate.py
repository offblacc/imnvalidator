import sys, json, os
import strategies
import asyncio
from util import start_process

### TODO PRIMARNI TEST - DA ČVOROVI U NODES ZAPRAVO POSTOJE U SIMULACIJI!!!!!!!!!!!!!!!!!!

async def main():
    if len(sys.argv) != 3:
        print("Missing scheme, test config or too many arguments")
        sys.exit(1)

    test_config = None
    with open(sys.argv[2], "r") as json_file:
        test_config = json.load(json_file)

    # run the simulation
    cmd = f"imunes -b {sys.argv[1]}; echo $?"

    print(f"Starting simulation")
    process = await start_process(cmd)

    # "live stream" simulation creation output
    # TODO also check for stderr.. now live streaming only from stdout, TEST IT by corrupting the imn file
    return_code, eid = None, None
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        pl = line.decode().strip()
        print(pl if pl not in ["0", "1"] else "")

        if pl.startswith("Experiment ID ="):
            eid = pl.split()[-1]
        return_code = pl

    # check return code

    if return_code != "0":
        print("Simulation failed to start")
        sys.exit(1) # TODO and cleanup?
    elif return_code == "0":
        # print(f'Simulation started successfully with eid={eid}')
        print(f"Simulation started successfully.")

    # output = await process.stdout.read() # old way, entire output at once

    # echo $? - 0 je uspjeh, 1 neuspjeh instanciranja simulacije
    # here is a messed up part... this will HAVE to be more modular, as you will have dynamic tests
    # sh f'imunes -b {sys.argv[1]}'

    # -----------------------------------------------------------------------------------------------

    # then go and run each operation...

    for test in test_config["tests"]:
        operation = strategies.assign_operation(test["test"])
        if operation is None: continue # add warning unsupported test
        await operation(
            eid,
            test["name"],
            test["fail"],
            test["success"],
            test["nodes"],
            test["expect"],
        )


if __name__ == "__main__":
    asyncio.run(main())
