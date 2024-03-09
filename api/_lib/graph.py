from .functions import lookup
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
    inputNodes = {}
    outputNodes = {}
    sortedInputs = inputSplitter(itemInputs)
    sortedOutputs = inputSplitter(finalOutputs)
    for item in sortedInputs["byproducts"]:
        item["unit"] = constants["itemUnit"]
        index = str(len(nodes))
        nodes.append(newNode(index, "byproduct", item))
        outputNodes[item["item"]] = index
    for item in sortedInputs["inputs"]:
        item["unit"] = constants["itemUnit"]
        index = str(len(nodes))
        nodes.append(newNode(index, "input", item))
        inputNodes[item["item"]] = index
    for item in sortedOutputs["byproducts"]:
        item["unit"] = constants["itemUnit"]
        index = str(len(nodes))
        nodes.append(newNode(index, "output", item))
        inputNodes[item["item"]] = index
    for item in sortedOutputs["inputs"]:
        item["unit"] = constants["itemUnit"]
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
        )
        for item in recipe["inputs"]:
            itemName = item["item"]
            itemAmount = item["amount"] * recipeQuantity
            details = {
                "item": itemName,
                "amount": itemAmount,
                "unit": constants["itemUnit"],
            }
            if itemName in inputNodes.keys():
                edges.append(
                    {
                        "start": inputNodes[itemName],
                        "end": recipeNodes[str(recipe["id"])],
                        "details": details,
                    }
                )
            if itemName in chosenRecipes["producing"].keys():
                edges.append(
                    {
                        "start": recipeNodes[str(chosenRecipes["producing"][itemName])],
                        "end": recipeNodes[str(recipe["id"])],
                        "details": details,
                    }
                )
        for item in recipe["outputs"]:
            itemName = item["item"]
            itemAmount = item["amount"] * recipeQuantity
            details = {
                "item": itemName,
                "amount": itemAmount,
                "unit": constants["itemUnit"],
            }
            if itemName in outputNodes.keys():
                edges.append(
                    {
                        "start": recipeNodes[recipe["id"]],
                        "end": outputNodes[itemName],
                        "details": details,
                    }
                )
            if itemName in chosenRecipes["consuming"].keys() and itemName not in chosenRecipes["producing"].keys():
                edges.append(
                    {
                        "start": recipeNodes[recipe["id"]],
                        "end": recipeNodes[chosenRecipes["consuming"][itemName]],
                        "details": details,
                    }
                )
    for item in finalOutputs:
        itemName = item["item"]
        itemAmount = item["amount"]
        details = {
            "item": itemName,
            "amount": item["amount"],
            "unit": constants["itemUnit"],
        }
        if itemAmount > 0 and itemName not in chosenRecipes["producing"].keys():
            edges.append(
                {
                    "start": inputNodes[itemName],
                    "end": outputNodes[itemName],
                    "details": details,
                }
            )
        if itemAmount < 0 and itemName not in chosenRecipes["consuming"].keys():
            edges.append(
                {
                    "start": outputNodes[itemName],
                    "end": inputNodes[itemName],
                    "details": details,
                }
            )
    return {"nodes": nodes, "edges": edges}
