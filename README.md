# RxGithubSearcher
This script demonstrates how to use ReactiveX to process a data stream asynchronously using it to retrive repositories information

## Requiers
* tornado
* pycurl
* rx (RxPy)

Tested on Python 3.5+

## Usage

To use it is necessary to get a Github API TOKEN as explained in the following page:
[Creating a personal access Token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line)

And then change the TOKEN on the config.py file

Run pip install -r requirements.txt to install the dependencies and run python server.py. 

The app will be served at http://localhost:8080/




