import sys, json, os
import strategies
import asyncio

def main():
    if len(sys.argv) != 3:
        print("Missing scheme, test config or too many arguments")
        sys.exit(1)
    
    test_config = None
    with open(sys.argv[2], 'r') as json_file:
        test_config = json.load(json_file)

    # run the simulation
    
    # here is a messed up part... this will HAVE to be more modular, as you will have dynamic tests
    os.popen("imunes -b " + sys.argv[1])
    
    
    # then go and run each operation...
    
    for test in test_config["tests"]:
        operation = strategies.assign_operation(test["test"])
        operation()
        #strategies.run_test(operation)
    
    
if __name__ == '__main__':
    main()
