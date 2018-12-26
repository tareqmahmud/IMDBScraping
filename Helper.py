import re


# Remove the space
def clean(item):
    return item.strip()


# Delete the min and remove the space
def clean_duration(duration):
    duration = re.findall(r"\d+", duration)[0]
    return int(duration)


# Delete the bracket and remove the space and make it int
def clean_year(year):
    year = re.findall(r"\d+", year)[0]
    return int(year)


# Delete , and return the int
def clean_gross(gross):
    if gross is not "Unknown":
        gross = re.findall(r"\d+", gross)
        gross = "".join(gross)
        return int(gross)
    else:
        return gross


# Str To Int
def metascore_to_int(item):
    if item is not "Unknown":
        return int(item)
    else:
        return item
