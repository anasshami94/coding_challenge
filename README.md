# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code

export GITHUB_USERNAME= <github-email-or-username>
export GITHUB_PASSWORD= <github-password>

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests
To get merged response from both git and bitbucket we implement this end point:

Functions supported:
* Get merged information about such team  
```
curl -i "http://127.0.0.1:5000/team?name=***"
or using any external client eg: postman
```

Not supported functions:
* Get branches, commits, clones 

* Get forked information

