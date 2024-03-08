# Functions for data acquisition
# Data from v1.3.1 (after reformatting)

from json import load
from .functions import currentValue
from .functions import lookup


def gameName(value: str, index: bool):
    games = {
        "coi": "Captain of Industry",
    }
    if index:
        return games[value]
    else:
        return list(games.keys())[list(games.values()).index(value)]


# getting data from data-list
def getRawData(game: str, parameter: str):
    fieldList = [
        "constants",
        "items",
        "machines",
        "recipes",
        "requirements",
    ]
    data = {}
    for field in fieldList:
        if parameter == field or parameter == None:
            fileName = "./api/data/" + gameName(game, False) + "/" + field + ".json"
            with open(fileName, "r", encoding="UTF-8") as dataFile:
                data[field] = load(dataFile)
    if parameter == None:
        return data
    else:
        return data[parameter]


def getData(game: str, gameSettings: dict[str:any] = {}, parameter: str = None):
    data = getRawData(game, parameter)

    def settingValue(setting: str) -> any:
        defaultValue = lookup(
            getRawData(game, "constants")["gameSettings"],
            "name",
            setting,
            "defaultValue",
        )
        return currentValue(gameSettings, setting, defaultValue)

    def nullFunction(value: any) -> any:
        return value

    def coiRecipes(recipes: list[dict]) -> list[dict]:
        for recipe in recipes:
            for item in recipe["outputs"]:
                if item["item"] == "Electricity":
                    item["amount"] *= settingValue("electricityMultiplier")
        return recipes

    reformattingFunctions = {
        "Captain of Industry": {
            "recipes": lambda value: coiRecipes(value),
        }
    }
    if parameter == None:
        for field in list(data.keys()):
            data[field] = currentValue(
                reformattingFunctions[game], field, lambda value: nullFunction(value)
            )(data[field])
    else:
        data = currentValue(
            reformattingFunctions[game], parameter, lambda value: nullFunction(value)
        )(data)
    return data
