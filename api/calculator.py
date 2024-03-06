# Main production calculator
# Functions based off v1.3.1

from .functions import currentValue
from .functions import lookup
from .functions import roundUp
from .functions import roundToDigit
from .functions import sign

# allowed recipe calculator
def allowedRecipes(
    item: str,
    amount: float,
    recipes: list[dict],
) -> list[dict]:
    searchSide = {-1: "inputs", 1: "outputs"}
    recipeType = sign(amount)
    allowedRecipeList = []
    for index in range(len(recipes)):
        for candidate in recipes[index][searchSide[recipeType]]:
            if item == candidate["item"]:
                allowedRecipeList.append(recipes[index])
    return allowedRecipeList


# MAIN CALCULATOR
def productionLine(
    chosenRecipes: dict[str, dict[str, str]],
    requiredItems: list[dict],
    recipes: list[dict],
) -> dict[str, list[dict]]:
    # set variables
    typeNames = {-1:"consuming",1:"producing"}
    recipeSides = ["inputs","outputs"]
    searchSide = {"producing": "inputs", "consuming": "outputs"}
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
        recipeTypeIndex = 1
        if excess[item] < 0:
            recipeTypeIndex *= -1
        if currentValue(production, item) * recipeTypeIndex < 0:
            recipeTypeIndex *= -1
        if (currentValue(production, item) + excess[item]) * recipeTypeIndex < 0:
            leftover = excess[item] + production[item]
            excess[item] = -production[item]
        else:
            leftover = 0
        recipeType = typeNames[recipeTypeIndex]
        production[item] = currentValue(production, item) + excess[item]
        recipeChosen = currentValue(chosenRecipes[recipeType], item, -1) != -1
        # working out values
        if recipeChosen:
            if abs(excess[item]) > 2**-32:  # to prevent diminishing loops
                recipeIndex = chosenRecipes[recipeType][item]
                itemRecipe = lookup(recipes, "id", recipeIndex)
                itemQuantity = lookup(
                    itemRecipe[searchSide[recipeType]], "item", item, "amount"
                )
                recipeQuantity = recipeTypeIndex * excess[item] / itemQuantity
                recipeAmounts[recipeIndex] = (
                    currentValue(recipeAmounts, recipeIndex) + recipeQuantity
                )
                for recipeSide in recipeSides:
                    for recipeItem in list(itemRecipe[recipeSide].keys()):
                        if recipeItem != item or recipeSide != searchSide[recipeType]:
                            excess[recipeItem] = (
                                currentValue(excess, recipeItem)
                                + excessFactors[recipeSide]
                                * recipeQuantity
                                * itemRecipe[recipeSide][recipeItem]
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
                {"recipeId": recipeIndex, "quantity": recipeAmounts[recipeIndex]}
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
        recipeMachine = lookup(recipes, "id", recipes[recipe["id"]], "machine")
        machineAmounts[recipeMachine] = (
            currentValue(machineAmounts, recipeMachine) + recipe["quantity"]
        )
    requirements = {}
    for machine in list(machineAmounts.keys()):
        for requirement in requirementList:
            requirements[requirement["name"]] = (
                currentValue(requirements, requirement)
                + requirementRounder(
                    machineAmounts[machine], requirement["utilisationDependency"]
                )
                * machines[machine]["requirements"][requirement]
            )
    machineRequirements = []
    for requirement in list(requirements.keys()):
        machineRequirements.append(
            {"requirement": requirement, "value": requirements[requirement]}
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
            byproducts.append({"item":item["item"],"amount":-item["amount"]})
    return {"inputs": inputs, "byproducts": byproducts}