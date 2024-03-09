from .functions import lookup
from .functions import sign
from .calculator import inputSplitter


def graphGenerator(
    recipeQuantities: list[dict],
    finalOutputs: list[dict],
    itemInputs: list[dict],
    recipeList: list[dict],
    chosenRecipes: dict[str, dict[str, str]],
    constants: dict[str, any],
):
    def newNode(index: str, nodeType: str, details: any):
        return {"id": index, "type": nodeType, "details": details}

    nodes = []
    # item nodes
    itemNodes = {}
    outputNodes = {}
    sortedInputs = inputSplitter(itemInputs)
    for item in sortedInputs["byproducts"]:
        index = str(len(nodes))
        nodes.append(newNode(index, "byproduct", item))
        itemNodes[item["item"]] = index
    for item in sortedInputs["inputs"]:
        index = str(len(nodes))
        nodes.append(newNode(index, "input", item))
        itemNodes[item["item"]] = index
    for item in finalOutputs:
        index = str(len(nodes))
        nodes.append(newNode(index, "output", item))
        outputNodes[item["item"]] = index
    # recipe nodes
    usedRecipes = []
    recipeNodes = {}
    for quantity in recipeQuantities:
        recipe = lookup(recipeList, "id", str(quantity["recipeId"]))
        recipeId = str(recipe["id"])
        usedRecipes.append(recipe)
        recipe["quantity"] = quantity["quantity"]
        index = str(len(nodes))
        nodes.append(newNode(index, "recipe", recipe))
        recipeNodes[recipeId] = index
    # edges
    edges = []
    for recipe in usedRecipes:
        recipeQuantity = (
            lookup(recipeQuantities, "recipeId", str(recipe["id"]), "quantity")
            * constants["unitFactor"]
            / recipe["duration"]
        )
        for item in recipe["inputs"]:
            itemName = item["item"]
            itemAmount = item["amount"] * recipeQuantity
            details = {
                "item": itemName,
                "amount": itemAmount,
                "unit": constants["itemUnit"],
            }
            if itemName in chosenRecipes["producing"].keys():
                startNode = recipeNodes[str(chosenRecipes["producing"][itemName])]
            else:
                startNode = itemNodes[itemName]
            edges.append(
                {
                    "start": startNode,
                    "end": recipeNodes[str(recipe["id"])],
                    "details": details,
                }
            )
        for item in recipe["outputs"]:
            itemName = item["item"]
            counted = True
            if itemName not in chosenRecipes["consuming"].keys():
                counted = False
                if itemName in lookup(finalOutputs, "item"):
                    endNode = outputNodes[itemName]
                else:
                    endNode = itemNodes[itemName]
            if not counted:
                details = {
                    "item": itemName,
                    "amount": item["amount"] * recipeQuantity,
                    "unit": constants["itemUnit"],
                }
                edges.append(
                    {
                        "start": recipeNodes[recipe["id"]],
                        "end": endNode,
                        "details": details,
                    }
                )
    for item in finalOutputs:
        details = {
            "item": item["item"],
            "amount": item["amount"],
            "unit": constants["itemUnit"],
        }
        if item["amount"] > 0 and item["item"] not in chosenRecipes["producing"].keys():
            edges.append(
                {
                    "start": itemNodes[item["item"]],
                    "end": outputNodes[item["item"]],
                    "details":details
                }
            )
        if item["amount"] < 0 and item["item"] not in chosenRecipes["consuming"].keys():
            edges.append(
                {
                    "start": outputNodes[item["item"]],
                    "end": itemNodes[item["item"]],
                    "details":details
                }
            )
    return {"nodes": nodes, "edges": edges}
