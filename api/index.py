from .data import getData
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def homepage():
  return getData("Captain of Industry", parameter="machines")

@app.route('/<game>/items')
def itemList(game):
  games = {
    "coi":"Captain of Industry",
  }
  return getData(games[game], parameter="items")