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
    elif returnField == None:
        return [value for value in lookupList if value[lookupField] == lookupValue]
    elif returnFirstOnly:
        matches = [
            value[returnField]
            for value in lookupList
            if value[lookupField] == lookupValue
        ]
        if len(matches) > 0:
            return matches[0]
        else:
            return ifNotFound
    else:
        return [
            value[returnField]
            for value in lookupList
            if value[lookupField] == lookupValue
        ]


# maths functions
def sign(value: float):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def roundUp(value: float):
    if value == int(value):
        value = int(value)
    else:
        value = int(value) + sign(value)
    return value


def roundToDigit(value: float, digits: int = 0, roundMode: str = "down"):
    value *= 10**digits
    if roundMode == "down":
        value = int(value)
    else:
        value = roundUp(value)
    value /= 10**digits
    return intConvert(value)


# integer coversions for printing values
def intConvert(value: float):
    if int(value) == value:
        value = int(value)
    return value
