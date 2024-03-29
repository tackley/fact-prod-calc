# General data-analysis functions
# Not really present in command-line version


# key-error free value for dictionaries
def currentValue(dictionary: dict, key: any, default: any = 0):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return default


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
        matches = [
            value
            for value in lookupList
            if value[lookupField] == lookupValue
        ]
    else: 
        matches = [
            value[returnField]
            for value in lookupList
            if value[lookupField] == lookupValue
        ]
    if returnFirstOnly:
        if len(matches) > 0:
            return matches[0]
        else:
            return ifNotFound
    else:
        return matches
        


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
