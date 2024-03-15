from flask import Flask
from flask import request
from ._lib.calculator import allowedRecipes
from ._lib.calculator import productionLine
from ._lib.calculator import totalRequirements
from ._lib.data import gameName
from ._lib.data import getData
from ._lib.functions import currentValue
from ._lib.graph import graphGenerator


app = Flask(__name__)


@app.route("/api")
def homepage() -> str:
    return "Welcome to the Factory Production Calculator v2.0!"


@app.route("/api/items", methods=["POST"])
def itemList() -> list[str]:
    # FORMATTING OF REQUEST:
    # {
    #     "settings": {
    #         settingName: settingValue,
    #         ...
    #     },
    #     "game": shortGameName,
    # }
    game = gameName(request.json["game"], True)
    gameSettings = currentValue(request.json, "settings", {})
    return getData(game, gameSettings, "items")


@app.route("/api/recipes", methods=["POST"])
def recipes() -> list[dict]:
    # FORMATTING OF REQUEST:
    # {
    #     "settings": {
    #         settingName: settingValue,
    #         ...
    #     },
    #     "game": shortGameName,
    #     "item": itemName,
    #     "nodeType": nodeType, (node type = "byproduct" or "input")
    # }
    gameSettings = currentValue(request.json, "settings", {})
    game = gameName(request.json["game"], True)
    itemName = request.json["item"]
    nodeType = request.json["nodeType"]
    return allowedRecipes(
        itemName, nodeType, getData(game, gameSettings, "recipes")
    )


@app.route("/api/calc", methods=["POST"])
def graph() -> dict[str:any]:
    # FORMATTING OF REQUEST:
    # {
    #     "chosenRecipes": {
    #         "input": {itemName: recipeId, ... }
    #         "byproduct": {itemName: recipeId, ... }
    #     },
    #     "outputItems": [
    #         {"item": name, "amount": amount},
    #         ...
    #     ],
    #     "settings": {
    #         settingName: settingValue,
    #         ...
    #     },
    #     "game": shortGameName,
    # }
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


@app.route("/api/settings", methods=["POST"])
def settings() -> list[dict]:
    # FORMATTING OF REQUEST:
    # {"game": shortGameName}
    game = gameName(request.json["game"], True)
    return getData(game, parameter="constants")["settings"]

@app.route("/api/item-unit", methods=["POST"])
def getItemUnit() -> str:
    # FORMATTING OF REQUEST:
    # {
    #     "settings": {
    #         settingName: settingValue,
    #         ...
    #     },
    #     "game": shortGameName,
    # }
    game = gameName(request.json["game"], True)
    settings = currentValue(request.json, "settings", {})
    return getData(game, settings, "constants")["itemUnit"]