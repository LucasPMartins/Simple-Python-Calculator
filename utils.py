import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def IsNumOrDot(string:str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def IsValidNumber(string:str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = valid
    return valid

def IsEmpty(string:str):
    return len(string) == 0