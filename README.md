# Coilgun
This project is a part of a Bachelor thesis at Chalmers University of Technology aimed at developing a more energy efficient coilgun. The aim of this project is to find the best values for all the parameters required when building a coilgun, such as coil-length, voltage etc, by using a genetic algorithm. 

## Installation
To install the project it is recommended to create a virtual environment for it first. Then you can open a terminal and run
```bash
git clone https://github.com/Paulsson99/coilgun.git
```
This will clone the repository to your current folder. To finish the installation download the requriements and install the repository with
```bash
# Change your current directory to the project folder
cd coilgun
# Install the requrements
pip install -r requirements.txt
# Make the project available everywhere in your environment
pip install -e .
```
You are now ready to start using the project. 

## How to use
The intended use case is to use commands from the command line. Right now only one command exists to visualise the coil. You use it like this
```bash
# This will show you what a coil would look like
vis coil

# This will start a simulation and show it to you
vis sim
```

## Developing
Before you start developing a new feature you should always start a new branch. When your feature is done create some tests for it and make sure they pass before creating a pull request. 

To run the test you do the following
```bash
# This will run all tests in the tests folder. Always do this before  a commit
pytest

# To run a specific file with tests use
pytest <path to file>
```

To get an overview of how much of the code that is covered by tests use
```bash
# This will print out a report of what percentage of files
# that are covered by tests
pytest --cov=src

# To generate a detailed report this command can be used.
# You can open the report by finding index.html in the folder htmlcov
# and open it in you webbrowser.
pytest --cov=src --cov-report html
```