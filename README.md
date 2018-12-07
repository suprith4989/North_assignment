# North_assignment
To complete the QA Take Home assignment for North

## Getting Started
### Using zip file
1. Download the wetransfer zip file 
2. Unzip the file using 'gunzip <filename>'
3. Run `pytest test_groupkt_api.py`

### Using github repo
1. Do a 'git clone https://github.com/suprith4989/North_assignment.git' locally to get the repo
2. Switch to the directory: 'cd Nort_assignment'
3. Build docker image using `docker build . -t api_test`
4. Run docker container using `docker run -it api_test bash`
5. Run tests in side the docker using `pytest-3 /root/test_groupkt_api.py -qsvvv`

### Using docker image
1. Pull the docker container using `docker pull <url>`
2. Run docker container `docker run -it api_test bash` 
3. Run tests in side the docker using `pytest-3 /root/test_groupkt_api.py -qsvvv`


### Prerequisites
- Docker must be installed on the system (If you are using docker)
- Python3, pytest should be installed in your system.

## Execution
1. Do a 'docker build . -t test_run'

## Author
**Suprith Gangawar 

