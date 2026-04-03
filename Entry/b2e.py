import BLL.bll as BLL
import BLL.util as UTIL
import Entry.ent as ENT

def b2e(bll: BLL.BLLfile):
    out = ENT.ENTfile()
    var_pos_gen = UTIL.var_position_generator()
    out._json["name"] = bll._name
    out._json["scenes"] = {
        "id": bll._id_gen.new_id(),
        "name": "Stage"
    }
    for var in bll._vars:
        out._json["variables"].append(var_build(var_pos_gen, var))
    return out

def var_build(pos_gen: UTIL.var_position_generator, var: BLL.BLLvar):
    out = dict()
    out["name"] = var._displayname
    out["id"] = var._id
    out["visible"] = False
    out["value"] = var._initial
    if var._type == "var":
        out["variableType"] = "variable"
        out["x"], out["y"] = pos_gen.new_var()
    elif var._type == "list":
        out["variableType"] = "list"
        out["x"], out["y"] = pos_gen.new_list()
        out["width"], out["height"] = 1200, 120
    out["isCloud"] = var._online
    out["isRealTime"] = False
    out["cloudDate"] = False
    out["object"] = None if var._dependency == "" else var._dependency
    return out