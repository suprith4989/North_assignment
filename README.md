# North_assignment
To complete the QA Take Home assignment for North

## Additional Information
* Given assignment is programmed using python programming language and is both python2 and python3 compatible
* It can be run in 3 different ways: 'unzipping the wetransfer zip file', 
'Cloning the git repo and manually executing the test file' and 'Directly pulling the image from my docker hub'.
* Last 2 functions in the script are a bit time consuming compared to the others, hence they are marked as skipped
* Overall 31 test cases should be run and displayed on the stdout
* Both positive and negative test cases are covered in the script
* No properietary software is used to complete the assignment
* pytest is the python framework 
## Getting Started / Build Instructions
Please follow 1 of below 3 instructions set to execute the test cases
### Using zip file
1. Download the wetransfer zip file 
2. Unzip the file using 'gunzip North_assignment.gz'
3. Switch to the unzipped directory
4. Run `pytest test_groupkt_api.py -qsvvv`

### Using github repo
1. Do a 'git clone https://github.com/suprith4989/North_assignment.git' locally to get the repo
2. Switch to the directory: 'cd Nort_assignment'
3. Build docker image using `docker build . -t api_test`
4. Run docker container using `docker run -it api_test bash`
5. Run tests in side the docker using `pytest-3 /root/test_groupkt_api.py -qsvvv`

### Using docker image
1. Pull the docker container using `docker pull suprith4989/groupkt_api_test`
2. Run docker container `docker run -it api_test bash` 
3. Run tests in side the docker using `pytest-3 /root/test_groupkt_api.py -qsvvv`

### Prerequisites
- Docker must be installed on the system (If you are using docker)
- Python3, pytest should be installed in your system.

## Author
**Suprith Gangawar <suprith_4989@yahoo.com>

