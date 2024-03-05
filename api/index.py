from .data import getData
from .functions import allowedRecipes
from flask import Flask
from flask import request

app = Flask(__name__)
games = {
  "coi":"Captain of Industry",
}
@app.route('/')
def homepage():
  return "Welcome to the Factory Production Calculator v2.0!"

@app.route('/<game>/items')
def itemList(game):
  return getData(games[game], parameter="items")

@app.route('/<game>/recipes', methods=["GET"])
def recipes(game):
  queryParameters = request.args
  item = queryParameters.get("item")
  amount = float(queryParameters.get("amount"))
  return allowedRecipes(item, amount, getData(games[game], parameter="recipes"))