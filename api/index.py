from .data import getData
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def homepage():
  return getData("Captain of Industry", parameter="machines")

@app.route('/items', methods=["GET"])
def homepage():
  queryParameters = request.args
  return getData(queryParameters.get("game"), parameter="items")