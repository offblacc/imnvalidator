# Imnvalidator
### IMUNES simulation validator/testing framework
This project is a testing framework for the IMUNES application. Its purpose is to simplify verifying a successful IMUNES installation and functionality (to test all functions work on, for example, a specific OS and hardware) as well as verify desired network operation for a specific simulation.

Instead of writing tests by programming and manually testing everything the network has to be able to do and what it must not be able to do, you can now just declare the desired functionalities in a JSON file and let the framework take care of the rest, reporting the status back to you.

There are two primary ways in which you can use the framework

### 1. Test IMUNES installation
The framework will provide an array of tests (JSON files and schemes, IMUNES .imn files). Running them should verify if the IMUNES installation is fully functioning and there are no bugs, whether IMUNES bugs or specific bugs caused by a specific operating system, libraries or hardware.
A quick and easy verification of a new IMUNES installation!

### 2. Validate successful network setup
When you need to setup a network a certain way, test firewalls, routing setups etc., instead of manual testing and/or writing a shell script that does the testing for you, you can just declare the tests in the JSON file, the desired network setup, and let the framework do the dirty work for you, saving you time.
Another goal this framework is trying to achieve is to simplify the process of testing student's work on an IMUNES simulation (homeworks, laboratory exercises, exams...), whether used by the student to test their network setup faster and easier or by the faculty to more easily check and grade the student's work.

> This part was implemented inside the project's scope, but is not addressed in this repo or is publicly available..:
> After the framework is done and working satisfactorily, some automation work needs to be done. The exact how and where is still to be determined.
>Also, maaaybe using Jenkins some remote testing, but that is still very undefined. It will depend on the needs and whether it will be considered practical or not.
>In the scope of the project a Jenkins server might be set up to run tests on X combinations of OS and hardware on remote agents, verifying a new IMUNES version itself.

## Installation
I'll assume you've installed Imunes, if not: https://github.com/imunes/imunes

Clone the repo:

```
git clone git@github.com:offblacc/imnvalidator.git
# OR
git clone https://github.com/offblacc/imnvalidator.git
```

Imnvalidator was written in Python 3, tested and developed using 3.11.

You'll need pip:

```
sudo apt update
#sudo apt install python3 # i assume you have it
sudo apt install python3-pip
```

And install pexpect:

```
pip install pexpect
```

You might have to, depending on your Python installation, use `pip3` or `python3 -m pip` instead of just `pip`.


## Usage
Basic usage is provided by passing --help to the framework:

```
$ python3 py/validate.py --help
usage: validate.py [-h] [-v] [-t] [-a] [imn_file] [config_file]

Run framework with specified arguments.

positional arguments:
  imn_file              Path to the imunes scheme
  config_file           Path to the JSON config file defining the tests

options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose mode
  -t, --timeit          Time the execution
  -a, --validate-installation
                        Validate imunes installation itself running all in
                        tests/
```

The framework can be used to validate an IMUNES installation by passing the argument `--validate-installation` or `-a`, or to validate a specific network setup by providing an .imn file and a JSON file with the desired tests.

Detailed explanation of the JSON files structure will be described in section one here as it belongs there and will be useful when explaining the second section. Easier to explain and write this way, so first let's tackle validating a specific network setup, then validating the IMUNES installation itself.

### 1. Validating a specific network setup
### 2. Validating IMUNES installation
To check whether your IMUNES installation is working properly, just run the framework with the `--validate-installation` or `-a` argument:

```
python3 py/validate.py -a
```

Output, cut for sanity sake (NOTE: the failed test checked for those packages on the host machine (not network nodes), for demo reasons, they are not necessary on the host for IMUNES to function):
```
Starting test big_simulation
Starting simulation
Simulation started successfully.

Running Test big simulation for errors
[PASS] Simulation started without warnings
Starting test check_install_host

Running Check multiple packages installed
...[FAIL] Command traceroute failed with non-zero exit: 1
...[FAIL] Command ifconfig failed with non-zero exit: 127
[FAIL] 0/2 successful checks
Starting test ping
Starting simulation
Simulation started successfully.

Running Ping pc1 to pc2
...[OK] Node 'pc1' pinged '10.0.0.22' successfully
[PASS] 1/1 pings successful
Starting test _services
Starting simulation
Simulation started successfully.


Running Test services
...[OK] FTP OK
...[OK] SSH OK
...[OK] TELNET OK
[PASS] 3/3 services test successful
Starting test traceroute
Starting simulation
Simulation started successfully.

Running Traceroute test
...[OK] pc1 -> 10.0.8.10 traceroute
...[OK] server -> 10.0.0.21 traceroute
[PASS] 2/2 traceroutes successful
Starting test check_install_node
Starting simulation
Simulation started successfully.

Running Check multiple packages installed
...[OK] Command traceroute on pc1 returned status 0
...[OK] Command ifconfig on pc1 returned status 0
...[OK] Command traceroute on pc2 returned status 0
...[OK] Command ifconfig on pc2 returned status 0
[PASS] 4/4 successful checks

Starting test _rip_validate
Starting simulation
Simulation started successfully.

Running Validate RIP funtioning
...[OK] Initial IPv4 ping goes through
...[OK] Initial IPv6 ping goes through
...[OK] Next RIP hop (IPv4) before turnoff is correct: 10.0.7.2
...[OK] Post turnoff IPv4 ping goes through
...[OK] Post turnoff IPv6 ping goes through
...[OK] Next RIP hop (IPv4) after turnoff is correct: 10.0.1.2
[PASS] RIP test successful

Number of failed tests: 1
Tests failed: check_install_host
```

When you see `Starting test X` for example `Starting test check_install_host`, that's the name of a specific 




#### Misc features
