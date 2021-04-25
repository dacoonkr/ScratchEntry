import utils.idgen as idgen

def convert(origin: dict, target = None, isList = False):
    ret = []
    varids = {}

    for i in origin:
        name = origin[i][0]
        
        if not isList:
            ret.append(getNewVar(name, str(origin[i][1]), target))
            print(f"Converted: Variable '{i}' to '{ret[-1]['id']}'")
        else:
            arr = []
            for j in origin[i][1]:
                arr.append({"data": j})
            ret.append(getNewList(name, arr, target))
            print(f"Converted: List '{i}' to '{ret[-1]['id']}'")

        varids[i] = ret[-1]["id"]

    return ret, varids

def getNewVar(name, value, target):
    var = {
        "name": name, "value": value, "id": idgen.getID(),
        "cloudDate": False,
        "isCloud": False,
        "isRealTime": False,
        "object": target,
        "variableType": "variable",
        "visible": False,
        "x": 0, "y": 0
    }
    return var

def getNewList(name, values, target):
    var = {
        "name": name, "value": 0, "id": idgen.getID(),
        "array": values,
        "cloudDate": False,
        "isCloud": False,
        "isRealTime": False,
        "object": target,
        "variableType": "list",
        "visible": False,
        "x": 0, "y": 0,
        "height": 120, "width": 100,
    }
    return var