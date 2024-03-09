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
def homepage() -> str:
    return "Welcome to the Factory Production Calculator v2.0!"


@app.route("/api/items", methods=["POST"])
def itemList() -> list[str]:
    game = gameName(request.json["game"], True)
    gameSettings = currentValue(request.json, "settings", {})
    return getData(game, gameSettings, "items")


@app.route("/api/recipes", methods=["POST"])
def recipes() -> list[dict]:
    recipeTypes = {"byproduct": "consuming", "input": "producing"}
    gameSettings = currentValue(request.json, "settings", {})
    game = gameName(request.json["game"], True)
    itemName = request.json["item"]
    recipeType = recipeTypes[request.json["nodeType"]]
    return allowedRecipes(
        itemName, recipeType, getData(game, gameSettings, "recipes")
    )


@app.route("/api/calculator", methods=["POST"])
def graph() -> dict[str:any]:
    # FORMATTING OF REQUEST:
    # {
    #     "chosenRecipes": {
    #         "producing": {itemName: recipeId, ... }
    #         "consuming": {itemName: recipeId, ... }
    #     },
    #     "outputItems": [
    #         {"item":itemName, "amount":itemAmount},
    #         ...
    #     ],
    #     "settings": {
    #         gameSetting: settingValue,
    #         ...
    #     },
    #     "game": shortGameName
    # }
    # (if not given, gameSettings will default to {}; all other fields are required)
    chosenRecipes = request.json["chosenRecipes"]
    outputItems = request.json["outputItems"]
    gameSettings = currentValue(request.json, "settings", {})
    game = gameName(request.json["game"], True)
    recipes = getData(game, gameSettings, "recipes")
    production = productionLine(
        chosenRecipes,
        outputItems,
        recipes,
        getData(game, gameSettings, "constants")["unitFactor"]
    )
    outputGraph = graphGenerator(
        production["recipes"],
        outputItems,
        production["inputs"],
        recipes,
        chosenRecipes,
        getData(game, gameSettings, "constants"),
    )
    requirements = totalRequirements(
        production["recipes"],
        recipes,
        getData(game, gameSettings, "machines"),
        getData(game, gameSettings, "requirements"),
    )
    return {"graph": outputGraph, "requirements": requirements}


@app.route("/api/settings/<game>")
def settings(game: str) -> list[dict]:
    return getData(gameName(game, True), parameter="constants")["settings"]
