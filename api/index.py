from flask import Flask
from flask import request
from .calculator import allowedRecipes
from .calculator import productionLine
from .calculator import totalRequirements
from .data import gameName
from .data import getData
from .functions import currentValue
from .graph import graphGenerator


app = Flask(__name__)

@app.route("/api")
def homepage():
    return "Welcome to the Factory Production Calculator v2.0!"

@app.route("/api/items/<game>")
def itemList(game):
    gameSettings = {} # not yet implemented
    return getData(gameName(game, True), gameSettings, "items")

@app.route("/api/recipes/<game>/<item>/<itemType>")
def recipes(game: str, item: str, itemType: str) -> list[dict]:
    # itemType = graph-node type
    recipeType = {"byproduct":"consuming", "input":"producing"}[itemType]
    gameSettings = {} # not yet implemented
    return allowedRecipes(
        item, recipeType, getData(gameName(game, True), gameSettings, "recipes")
    )

@app.route("/api/calculator/<game>", method=["POST"])
def graph(game: str) -> dict[str:any]:
    # expects game as short name (e.g. coi)
    inputData = request.json
    # FORMATTING OF REQUEST:
    # {
    #     "chosenRecipes": {
    #         "producing": [{itemName: recipeId, ... }]
    #         "consuming": [{itemName: recipeId, ... }]
    #     },
    #     "outputItems": [
    #         {"item":itemName, "amount":itemAmount},
    #         ...
    #     ],
    #     "gameSettings": {
    #         gameSetting: settingValue,
    #         ...
    #     },
    # }
    # (if not given, gameSettings will default to {}; all other fields are required)
    chosenRecipes = inputData["chosenRecipes"]
    outputItems = inputData["outputItems"]
    gameSettings = currentValue(inputData, "gameSettings", {})
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
