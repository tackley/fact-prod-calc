from flask import Flask
from flask import request
from .calculator import allowedRecipes
from .calculator import productionLine
from .calculator import totalRequirements
from .data import gameName
from .data import getData
from .graph import graphGenerator


app = Flask(__name__)

# Game settings must be added to all functions
@app.route("/api")
def homepage():
    return "Welcome to the Factory Production Calculator v2.0!"

@app.route("/api/items/<game>")
def itemList(game):
    gameSettings = {}
    return getData(gameName(game, True), gameSettings, "items")

@app.route("/api/recipes/<game>/<item>")
def recipes(game: str, item: str) -> list[dict]:
    gameSettings = {}
    queryParameters = request.args
    amount = float(queryParameters.get("amount"))
    return allowedRecipes(
        item, amount, getData(gameName(game, True), gameSettings, "recipes")
    )

# Must input dictionaries here; should they just be query parameters? Or something fancier?
# (also needed for game settings)
@app.route("/api/calculator/<game>")
def graph(game: str, chosenRecipes: dict[str, dict[str, str]], outputItems: list[dict]):
    gameSettings = {}
    game = gameName(game, True)
    recipes = getData(game, gameSettings, "recipes")
    production = productionLine(chosenRecipes, outputItems, recipes)
    outputGraph = graphGenerator(
        production["recipes"],
        outputItems,
        production["inputs"],
        recipes,
        chosenRecipes,
        getData(game, gameSettings, "constants"),
    )
    requirements = totalRequirements(
        production[recipes],
        recipes,
        getData(game, gameSettings, "machines"),
        getData(game, gameSettings, "requirements"),
    )
    return {"graph": outputGraph, "requirements": requirements}