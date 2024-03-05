from .data import getData
from .calculator import allowedRecipes
from flask import Flask
from .data import gameName
from flask import request

app = Flask(__name__)
@app.route('/')
def homepage():
  return "Welcome to the Factory Production Calculator v2.0!"

@app.route('/<game>/items')
def itemList(game):
  return getData(gameName(game,True), parameter="items")

@app.route('/<game>/recipes', methods=["GET"])
def recipes(game):
    queryParameters = request.args
    item = queryParameters.get("item")
    amount = float(queryParameters.get("amount"))
    return allowedRecipes(item, amount, getData(gameName(game,True), parameter="recipes"))