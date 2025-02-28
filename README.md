# Diplomski / Master's thesis

This project is a testing framework for the IMUNES application. Its purpose is to simplify verifying a successfull IMUNES installation and functionality (to test all functions work on, for example, a specific OS and hardware) as well as verify desired network operation for a specific simulation.

Instead of writing tests by programming and manually testing everything the network has to be able to do and what it must not be able to do, you can now just declare the desired functionalities in the JSON file and let the framework take care of the rest, reporting the status back to you.

When the first version of the framework is fully functional, it will be used in two ways (although, the second way of using it, as defined below, is only enabling the first specified way of using it).

## 1. Test IMUNES installation
The framework will provide an array of tests (JSON files and schemes, IMUNES .imn files). Running them should verify if the IMUNES installation is fully functioning and there are no bugs, whether IMUNES bugs or specific bugs caused by a specific operating system, libraries or hardware.
A quick and easy verification of a new IMUNES installation!

## 2. Validate successful network setup
When you need to setup a network a certain way, test firewalls, routing setups etc., instead of manual testing and/or writing a shell script that does the testing for you, you can just declare the tests in the JSON file, the desired network setup, and let the framework do the dirty work for you, saving you time.
Another goal this framework is trying to achieve is to simplify the process of testing student's work on an IMUNES simulation (homeworks, laboratory exercises, exams...), whether used by the student to test their network setup faster and easier or by the faculty to more easily check and grade the student's work.

After the framework is done and working satisfactorily, some automation work needs to be done. The exact how and where is still to be determined.
Also, maaaybe using Jenkins some remote testing, but that is still very undefined. It will depend on the needs and whether it will be considered practical or not.
In the scope of the project a Jenkins server might be set up to run tests on X combinations of OS and hardware on remote agents, verifying a new IMUNES version itself.