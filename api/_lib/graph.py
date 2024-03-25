from .functions import lookup
from .functions import roundToDigit
from .calculator import allowedRecipes, inputSplitter


def graphGenerator(
    recipeQuantities: list[dict],
    finalOutputs: list[dict],
    itemInputs: list[dict],
    recipeList: list[dict],
    chosenRecipes: dict[str, dict[str, str]],
    constants: dict[str, any],
):
    nodes = []

    def newNode(nodeType: str, labelInfo: any):
        nodeColours = {
            "input": "#FFC080",
            "input-end": "#C0C0C0",
            "byproduct": "#FFC080",
            "byproduct-end": "#C0C0C0",
            "output": "#80FFC0",
            "recipe": "#80C0FF",
        }
        nodes.append(
            {
                "id": str(len(nodes)),
                "type": nodeType,
                "color": nodeColours[nodeType],
                "x": (len(nodes) % 10) * 100,
                "y": len(nodes) * 10,
                "labelInfo": labelInfo,
            }
        )

    # item nodes
    inputNodes = {}
    outputNodes = {}
    sortedInputs = inputSplitter(itemInputs)
    sortedOutputs = inputSplitter(finalOutputs)
    for item in sortedInputs["byproducts"]:
        item["unit"] = constants["itemUnit"]
        outputNodes[item["item"]] = str(len(nodes))
        if len(allowedRecipes(item["item"], "byproduct", recipeList)) == 0:
            nodeType = "byproduct-end"
        else:
            nodeType = "byproduct"
        newNode(nodeType, item)
    for item in sortedInputs["inputs"]:
        item["unit"] = constants["itemUnit"]
        inputNodes[item["item"]] = str(len(nodes))
        if len(allowedRecipes(item["item"], "input", recipeList)) == 0:
            nodeType = "input-end"
        else:
            nodeType = "input"
        newNode(nodeType, item)
    for item in sortedOutputs["byproducts"]:
        item["unit"] = constants["itemUnit"]
        inputNodes[item["item"]] = str(len(nodes))
        newNode("output", item)
    for item in sortedOutputs["inputs"]:
        item["unit"] = constants["itemUnit"]
        outputNodes[item["item"]] = str(len(nodes))
        newNode("output", item)
    # recipe nodes
    usedRecipes = []
    recipeNodes = {}
    for quantity in recipeQuantities:
        recipe = lookup(recipeList, "id", quantity["recipeId"])
        usedRecipes.append(recipe)
        recipe["quantity"] = quantity["quantity"]
        recipeNodes[recipe["id"]] = str(len(nodes))
        newNode("recipe", recipe)
    # edges
    edges = []

    def newEdge(source: str, target: str, item: dict[str, any]):
        edges.append(
            {
                "source": source,
                "target": target,
                "label": str(roundToDigit(item["amount"], 2, "up"))
                + constants["itemUnit"]
                + " "
                + item["item"],
            }
        )

    for recipe in usedRecipes:
        recipeId = recipe["id"]
        recipeQuantity = lookup(recipeQuantities, "recipeId", recipeId, "quantity")
        for item in recipe["inputs"][:]:
            itemName = item["item"]
            item["amount"] *= recipeQuantity
            if itemName in inputNodes.keys():
                newEdge(
                    inputNodes[itemName],
                    recipeNodes[recipeId],
                    item,
                )
            elif itemName in chosenRecipes["input"].keys():
                newEdge(
                    recipeNodes[chosenRecipes["input"][itemName]],
                    recipeNodes[recipeId],
                    item,
                )
            else:
                recipeFound = False
                for testRecipe in usedRecipes:
                    if itemName in lookup(testRecipe["outputs"], "item"):
                        sourceRecipe = testRecipe["id"]
                        recipeFound = True
                if recipeFound:
                    newEdge(
                        recipeNodes[sourceRecipe],
                        recipeNodes[recipeId],
                        item,
                    )
        for item in recipe["outputs"][:]:
            itemName = item["item"]
            item["amount"] *= recipeQuantity
            if itemName in outputNodes.keys():
                newEdge(
                    recipeNodes[recipeId],
                    outputNodes[itemName],
                    item,
                )
            elif (
                itemName in chosenRecipes["byproduct"].keys()
                and itemName not in chosenRecipes["input"].keys()
            ):
                newEdge(
                    recipeNodes[recipeId],
                    recipeNodes[chosenRecipes["byproduct"][itemName]],
                    item,
                )

    for item in finalOutputs:
        itemAmount = item["amount"]
        itemName = item["item"]
        if itemAmount > 0 and itemName not in chosenRecipes["input"].keys():
            newEdge(inputNodes[itemName], outputNodes[itemName], item)
        if itemAmount < 0 and itemName not in chosenRecipes["byproduct"].keys():
            newEdge(outputNodes[itemName], inputNodes[itemName], item)
    return {"nodes": nodes, "edges": edges}
