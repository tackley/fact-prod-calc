# Main production calculator
# Production line function based off v1.3.1

from .functions import currentValue
from .functions import lookup
from .functions import roundUp
from .functions import roundToDigit


# allowed recipe calculator
def allowedRecipes(
    item: str,
    nodeType: str,
    recipes: list[dict],
) -> list[dict]:
    searchSide = {"byproduct": "inputs", "input": "outputs"}
    allowedRecipeList = []
    for recipe in recipes:
        for candidate in recipe[searchSide[nodeType]]:
            if item == candidate["item"]:
                allowedRecipeList.append(recipe)
    return allowedRecipeList


# MAIN CALCULATOR
def productionLine(
    chosenRecipes: dict[str, dict[str, str]],
    requiredItems: list[dict],
    recipes: list[dict],
    unitFactor: float,
) -> dict[str, list[dict]]:
    # set variables
    typeNames = {-1: "byproduct", 1: "input"}
    recipeSides = ["inputs", "outputs"]
    searchSides = {"input": "outputs", "byproduct": "inputs"}
    excessFactors = {"inputs": 1, "outputs": -1}
    finalProducts = {}
    recipeAmounts = {}
    zeroes = []
    # input-dependent variables
    checklist = lookup(requiredItems, "item")
    for index in range(len(checklist)):
        zeroes.append(0)
    production = dict(zip(checklist, zeroes))
    excess = dict(zip(lookup(requiredItems, "item"), lookup(requiredItems, "amount")))
    # iterator section
    while len(checklist) > 0:
        item = checklist[0]
        # recipe type
        itemTypeIndex = 1
        if excess[item] < 0:
            itemTypeIndex *= -1
        if currentValue(production, item) * itemTypeIndex < 0:
            itemTypeIndex *= -1
        if (currentValue(production, item) + excess[item]) * itemTypeIndex < 0:
            leftover = excess[item] + production[item]
            excess[item] = -production[item]
        else:
            leftover = 0
        itemType = typeNames[itemTypeIndex]
        searchSide = searchSides[itemType]
        production[item] = currentValue(production, item) + excess[item]
        recipeChosen = currentValue(chosenRecipes[itemType], item, None) != None
        # working out values
        if recipeChosen:
            if abs(excess[item]) > 2**-32:  # to prevent diminishing loops
                recipeIndex = str(chosenRecipes[itemType][item])
                itemRecipe = lookup(recipes, "id", recipeIndex)
                itemQuantity = lookup(
                    itemRecipe[searchSide], "item", item, "amount"
                )
                recipeQuantity = (
                    itemTypeIndex
                    * excess[item]
                    / itemQuantity
                )
                recipeAmounts[recipeIndex] = (
                    currentValue(recipeAmounts, recipeIndex) + recipeQuantity
                )
                for recipeSide in recipeSides:
                    for recipeItem in lookup(itemRecipe[recipeSide], "item"):
                        if recipeItem != item or recipeSide != searchSide:
                            excess[recipeItem] = currentValue(
                                excess, recipeItem
                            ) + excessFactors[recipeSide] * recipeQuantity * lookup(
                                itemRecipe[recipeSide], "item", recipeItem, "amount"
                            )
                            if recipeItem not in checklist:
                                checklist.append(recipeItem)
        else:  # item removal
            finalProducts[item] = currentValue(finalProducts, item) + excess[item]
        if leftover == 0:
            excess.pop(item)
            checklist.remove(item)
        else:
            excess[item] = leftover
    # reformatting outputs
    itemInputs = []
    for item in list(finalProducts.keys()):
        if finalProducts[item] != 0:
            itemInputs.append({"item": item, "amount": finalProducts[item]})
    recipeQuantities = []
    for recipeIndex in list(recipeAmounts.keys()):
        if recipeAmounts[recipeIndex] != 0:
            recipeQuantities.append(
                {
                    "recipeId": recipeIndex,
                    "quantity": recipeAmounts[recipeIndex] * lookup(recipes, "id", recipeIndex, "duration") / unitFactor
                }
            )
    return {
        "inputs": itemInputs,
        "recipes": recipeQuantities,
    }


# selective rounding of machine numbers
def requirementRounder(quantity: float, utilisationDependency: bool) -> float:
    if not utilisationDependency:
        quantity = roundUp(quantity)
    return quantity


# machine requirement calculator
def totalRequirements(
    recipeQuantities: list[dict],
    recipes: list[dict],
    machines: list[dict],
    requirementList: list[dict],
) -> list[dict]:
    machineAmounts = {}
    for recipe in recipeQuantities:
        recipeMachine = lookup(recipes, "id", recipe["recipeId"], "machine")
        machineAmounts[recipeMachine] = (
            currentValue(machineAmounts, recipeMachine) + recipe["quantity"]
        )
    requirements = {}
    for machine in list(machineAmounts.keys()):
        for requirement in requirementList:
            requirements[requirement["name"]] = (
                currentValue(requirements, requirement["name"])
                + requirementRounder(
                    machineAmounts[machine], requirement["utilisationDependency"]
                )
                * lookup(machines, "name", machine)["requirements"][requirement["name"]]
            )
    machineRequirements = []
    for requirement in lookup(requirementList, "name"):
        if currentValue(requirements, requirement) != 0:
            machineRequirements.append(
                {
                    "requirement": requirement,
                    "value": requirements[requirement],
                    "unit": lookup(requirementList, "name", requirement, "unit", ifNotFound=""),
                }
            )
    return machineRequirements


# output of machine requirements
def requirementStrings(
    totalRequirements: list[dict], requirementList: list[dict]
) -> list[str]:
    outputStrings = []
    for requirement in lookup(totalRequirements, "name"):
        requirementUnit = lookup(requirementList, "name", requirement, "unit")
        outputStrings.append(
            roundToDigit(totalRequirements, 2, "up")
            + requirementUnit
            + " "
            + requirement
        )
    return outputStrings


def inputSplitter(itemInputs: list[dict]) -> dict[str, list[dict]]:
    inputs = []
    byproducts = []
    for item in itemInputs:
        if item["amount"] > 0:
            inputs.append({"item": item["item"], "amount": item["amount"]})
        if item["amount"] < 0:
            byproducts.append({"item": item["item"], "amount": -item["amount"]})
    return {"inputs": inputs, "byproducts": byproducts}
