#-------------------------------------------------------------------------------------------------------------------------------
def removePrefix(string, prefix):
    if not string.startswith(prefix):
        return string

    return string[len(prefix):]

#-------------------------------------------------------------------------------------------------------------------------------
def ensureJSONSchema(schema, jsoncontent):
    isClean = True

    for key in schema:
        if key not in jsoncontent:
            isClean = False
            jsoncontent[key] = schema[key]
    return isClean

#-------------------------------------------------------------------------------------------------------------------------------
def timeDifferenceInMinutes(lastTimeDate,currentTimeDate):
    #timeDelta = lastTimeDate - currentTimeDate
    timeDelta = currentTimeDate - lastTimeDate
    timeMinutes = int(timeDelta.total_seconds() / 60)
    print (f'Time Difference : {timeMinutes}')
    return timeMinutes

def timeDifferenceInSeconds(lastTimeDate,currentTimeDate):
    #timeDelta = lastTimeDate - currentTimeDate
    timeDelta = currentTimeDate - lastTimeDate
    timeSeconds = int(timeDelta.total_seconds())
    print (f'Time Difference : {timeSeconds}')
    return timeSeconds
