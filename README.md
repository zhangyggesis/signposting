Do the following to add the REST API

Install flask and flask request

python3 -m pip install Flask
python3 -m pip install flask-requests
-------------
pip install Flask
pip install flask-requests


# import the flask module in python
from flask import Flask, request
app = Flask(__name__)

execute command in the src directiory

python3 -m flask --app controller run --port 8000 --debug
