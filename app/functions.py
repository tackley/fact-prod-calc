# Factory Production Calculator v2.0 BACKEND
# Based off version 1.3.1 (2024-03-03)

# key-error free value for dictionaries
def currentValue(dictionary: dict, key: any, default: any = 0):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return default

# # item unit setter (per time-unit vs per recipe)
# print()
# print(f"Would you like item values to be shown {itemUnitLong}, or for the recipe's duration?")
# print(f"Type 'y' for {itemUnitLong}; 'n' for recipe duration:")
# perDuration = boolean[str(input(">>> "))]
# print()

# # chosen recipes table
# notChosen = []
# notFinal = []
# for index in range(0, len(items.keys())):
#     notChosen.append(-1)
#     notFinal.append(False)
# chosenRecipes = {
#     1: dict(zip(list(items.keys()), notChosen)), # production recipes
#     -1: dict(zip(list(items.keys()), notChosen)), # consumption recipes
# }

# lookup in dictionary-lists
def lookup(
    lookupList: list[dict],
    lookupField: any,
    lookupValue: any = None,
    returnField: any = None,
    returnFirstOnly: bool = True,
    ifNotFound: any = None,
):
    if lookupValue == None:
        return [value[lookupField] for value in lookupList]
    else:
        output = [
            value[lookupField]
            for value in lookupList
            if value[returnField] == lookupValue
        ]
        if returnFirstOnly:
            if len(output) > 0:
                return output[0]
            else:
                return ifNotFound
        else:
            return output

# allowed recipe calculator
def allowedRecipes(item: str, amount: float, recipes: list):
    searchSide = {-1: "inputs", 1: "outputs"}
    recipeType = 1
    if amount < 0:
        recipeType *= -1
    allowedRecipeList = []
    for index in range(len(recipes)):
        for candidate in recipes[index][searchSide[recipeType]]:
            if item == candidate["item"]:
                allowedRecipeList.append(recipes[index])
    return allowedRecipeList

# MAIN CALCULATOR
def productionLine(chosenRecipes: dict[int, dict[str, str]], requiredItems: dict, recipes: list) -> dict:
    textIndex = {0: "inputs", 1: "outputs"}
    searchSide = {-1: "inputs", 1: "outputs"}
    excessFactors = {0: 1, 1: -1}
    finalProducts = {}
    recipeAmounts = {}
    zeroes = []
    for index in range(len(list(requiredItems.keys()))):
        zeroes.append(0)
    production = dict(zip(list(requiredItems.keys()), zeroes))
    excess = requiredItems.copy()
    checklist = list(requiredItems.keys())
    while len(checklist) > 0:
        item = checklist[0]
        # recipe type
        recipeType = 1
        if excess[item] < 0:
            recipeType *= -1
        if currentValue(production, item) * recipeType < 0:
            recipeType *= -1
        if (currentValue(production, item) + excess[item]) * recipeType < 0:
            leftover = excess[item] + production[item]
            excess[item] = -production[item]
        else:
            leftover = 0
        production[item] = currentValue(production, item) + excess[item]
        recipeChosen = currentValue(chosenRecipes[recipeType], item, -1) != -1
        # working out values
        if recipeChosen:
            if abs(excess[item]) > 2**-32:  # to prevent diminishing loops
                recipeIndex = chosenRecipes[recipeType][item]
                itemRecipe = recipes[recipeIndex]
                itemQuantity = lookup(
                    item, itemRecipe[searchSide[recipeType]], "item", "amount"
                )
                recipeQuantity = recipeType * excess[item] / itemQuantity
                recipeAmounts[recipeIndex] = (
                    currentValue(recipeAmounts, recipeIndex) + recipeQuantity
                )
                for recipeSideIndex in range(1):
                    recipeSide = textIndex[recipeSideIndex]
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
    productionRates = []
    for item in list(production.keys()):
        if production[item] != 0:
            productionRates.append({"item": item, "amount": production[item]})
    requiredInputs = []
    for item in list(finalProducts.keys()):
        if finalProducts[item] != 0:
            requiredInputs.append({"item": item, "amount": finalProducts[item]})
    recipeQuantities = []
    for recipeIndex in list(recipeAmounts.keys()):
        if recipeAmounts[recipeIndex] != 0:
            recipeQuantities.append(
                {"recipeId": recipeIndex, "quantity": recipeAmounts[recipeIndex]}
            )
    return {
        "productionRates": productionRates,
        "requiredInputs": requiredInputs,
        "recipes": recipeQuantities,
    }


# maths functions
def sign(value: int | float):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def roundUp(value: int | float):
    if value == int(value):
        value = int(value)
    else:
        value = int(value) + sign(value)
    return value


def roundToDigit(value: int | float, digits: int = 0, roundMode: str = "down"):
    value *= 10**digits
    if roundMode == "down":
        value = int(value)
    else:
        value = roundUp(value)
    value /= 10**digits
    return intConvert(value)


# integer coversions for printing values
def intConvert(value: int | float):
    if int(value) == value:
        value = int(value)
    return value


# selective rounding of machine numbers
def requirementRounder(quantity: int | float, utilisationDependency: bool):
    if not utilisationDependency:
        quantity = roundUp(quantity)
    return quantity


# machine quantity aggregator and requirement calculator
def machineCalculator(
    recipeQuantities: list[dict],
    recipes: list[dict],
    machines: list[dict],
    requirementList: list[dict],
):
    machineAmounts = {}
    for recipe in recipeQuantities:
        recipeMachine = lookup(recipes, "id", recipes[recipe["recipeId"]], "machine")
        machineAmounts[recipeMachine] = (
            currentValue(machineAmounts, recipeMachine) + recipe["quantity"]
        )
    requirements = {}
    machineQuantities = []
    for machine in list(machineAmounts.keys()):
        machineQuantities.append(
            {"machine": machine, "quantity": machineAmounts[machine]}
        )
        for requirement in lookup(requirementList, "name"):
            requirements[requirement] = (
                currentValue(requirements, requirement)
                + requirementRounder(
                    machineAmounts[machine],
                    lookup(
                        requirementList, "name", requirement, "utilisationDependency"
                    ),
                )
                * machines[machine]["requirements"][requirement]
            )
    machineRequirements = []
    for requirement in list(requirements.keys()):
        machineRequirements.append(
            {"requirement": requirement, "value": requirements[requirement]}
        )
    return {"quantities": machineQuantities, "requirements": machineRequirements}

# output of machine requirements
def requirementStrings(totalRequirements: list[dict], requirementList: list[dict]):
    outputStrings = []
    for requirement in lookup(totalRequirements, "name"):
        requirementUnit = lookup(requirementList, "name", requirement, "unit")
        outputStrings.append(
            roundToDigit(totalRequirements, 2, "up") + requirementUnit + requirement
        )
    return outputStrings