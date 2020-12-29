import os
def getBool(key: str, default: bool=None):
    if key not in os.environ:
        return default
    else:
        envValue = os.environ[key]
        if envValue  == "True": return True
        elif envValue == "False": return False
        else: return default

def getInt(key: str, default: int=None):
    if key not in os.environ:
        return default
    else:
        try:
            return int(os.environ[key])
        except:
            return default