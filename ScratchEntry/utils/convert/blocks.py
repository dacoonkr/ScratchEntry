import utils.idgen as idgen
import utils.convert.procedures as procedures
import utils.convert.macro.macros as macros

import json

def convert(origin: dict, libs, object_number):
    blockids = {}
    header = []
    functions = []

    for i in origin:
        blockids[i] = idgen.getID()

        block = origin[i]
        ret = libs.find(block["opcode"])
        if ret != None:
            if ret["type"] == "header":
                header.append(i)
                continue
        if "parent" in block:
            if block["parent"] == None:
                print(f"HEADER MISS! {block['opcode']}")

    ret = []
    for i in header:
        if origin[i]["opcode"] == "procedures_definition":
            functions.append([procedures.convert(i, origin, libs, object_number), 
                              origin[origin[i]["inputs"]["custom_block"][1]]["mutation"]["proccode"]])
        else:
            ret.append(chunkTrace(i, blockids, origin, libs, {}, object_number))

    return ret, functions

def chunkTrace(cur, blockids, origin, libs, fn_args, object_number):
    if cur == None: return

    ret = []
    while True:
        if origin[cur]["opcode"] == "argument_reporter_string_number" or origin[cur]["opcode"] == "argument_reporter_boolean":
            name = origin[cur]["fields"]["VALUE"][0]
            if not name in fn_args:
                ret.append(getblock(idgen.getID(), "number", [0]))
            else: 
                ret.append(getblock(blockids[cur], fn_args[name], [None]))
        elif origin[cur]["opcode"] == "procedures_call":
            args = json.loads(origin[cur]["mutation"]["argumentids"])
            fnid = libs.get_fn(origin[cur]["mutation"]["proccode"])
            params = []
            for argid in args:
                params.append(paramTrace(origin[cur]["inputs"][argid], blockids, origin, libs, fn_args, object_number))
            ret.append(getblock(blockids[cur], f"func_{fnid}", params + [None]))
        else:
            found = libs.find(origin[cur]["opcode"])
            if found != None:
                params = []
                for x in found["params"]:
                    if x[0] == '"':
                        params.append(x[1:])
                    elif x[0] == '#':
                        fields, dicts = x[1:].split(";")
                        after = json.loads(dicts)
                        before = origin[cur]["fields"][fields][0]
                        if before in after:
                            params.append(after[before])
                        else:
                            params.append(before)
                    elif x[0:2] == '!!':
                        params.append(libs.get_brd(origin[cur]["fields"]["BROADCAST_OPTION"][1]))
                    elif x[0] == '>':
                        data = origin[origin[cur]["inputs"]["CLONE_OPTION"][1]]["fields"]["CLONE_OPTION"][0]
                        if data == "_myself_": data = "self"
                        else: data = libs.get_spt(data)
                        params.append(data)
                    elif x[0] == '!':
                        params.append(libs.get_brd(origin[cur]["inputs"]["BROADCAST_INPUT"][1][2]))
                    elif x[0] == '^':
                        data = origin[cur]["inputs"]["COSTUME"][1]
                        if type(data) == list: 
                            params.append(getblock(idgen.getID(), "get_pictures", [paramTrace(data, blockids, origin, libs, fn_args, object_number)]))
                        else:
                            params.append(getblock(idgen.getID(), "get_pictures", [libs.get_costume(object_number, origin[data]["fields"]["COSTUME"][0])]))
                    elif x[0] == '*':
                        dat = origin[origin[cur]["inputs"][x[1:]][1]]["fields"][x[1:]][0]
                        if x[1:] == "TOUCHINGOBJECTMENU":
                            params.append(libs.get_spt(dat))
                        if x[1:] == "KEY_OPTION":
                            params.append(libs.keyconvert(dat))
                    elif x == '&VARIABLE' or x == '&LIST':
                        params.append(libs.get_var(origin[cur]["fields"][x[1:]][1]))
                    elif x == '&NULL':
                        params.append(None)
                    else:
                        d = paramTrace(origin[cur]["inputs"][x], blockids, origin, libs, fn_args, object_number)
                        params.append(d)
                if found["type"] == "direct" or found["type"] == "operator" or found["type"] == "header":
                    if found["code"] == "boolean_not":
                        ret.append(getblock(blockids[cur], found["code"], params[1] + [None]))
                    ret.append(getblock(blockids[cur], found["code"], params + [None]))

                elif found["type"] == "substk":
                    if "SUBSTACK" in origin[cur]["inputs"]:
                        substk = paramTrace(origin[cur]["inputs"]["SUBSTACK"], blockids, origin, libs, fn_args, object_number)
                    else: substk = []

                    if found["code"] == "if_else" or found["code"] == "_if" or found["code"] == "repeat_while_true":
                        substk2 = None
                        if found["code"] == "if_else":
                            if not "SUBSTACK2" in origin[cur]["inputs"]:
                                substk2 = []
                            else: substk2 = paramTrace(origin[cur]["inputs"]["SUBSTACK2"], blockids, origin, libs, fn_args, object_number)
                        if params == [[]]:
                            print(f"stop by {cur}")
                        ret.append(getblock(blockids[cur], found["code"], [params[0][0], None], statement = [substk, substk2]))
                    else:
                        ret.append(getblock(blockids[cur], found["code"], params + [None], statement = [substk]))

                elif found["type"] == "macro":
                    if found["code"] == "resetlist":
                        fn_definition, fn_call = macros.resetlist(params[0])
                        ret.append(fn_definition)
                        ret.append(fn_call)

            else:
                print(f"BLOCK MISS! {origin[cur]['opcode']}")

        #print(f"Converted: Block '{cur}'")

        if origin[cur]["next"] == None: break
        cur = origin[cur]["next"]

    return ret

def paramTrace(inputs, blockids, origin, libs, fn_args, object_number):
    if inputs[0] == 1:
        if inputs[1] == None:
            return getblock(idgen.getID(), "text", [""])
        return getblock(idgen.getID(), "text", [str(inputs[1][1])])
    elif inputs[0] == 4:
        return getblock(idgen.getID(), "number", [inputs[1][1]])
    elif inputs[0] == 3:
        if inputs[1][0] == 12:
            ret = getblock(idgen.getID(), "get_variable", [libs.get_var(inputs[1][2]), None])
            return ret
        else:
            ret = chunkTrace(inputs[1], blockids, origin, libs, fn_args, object_number)
            if len(ret) == 0: return []
            return ret[0]
    elif inputs[0] == 2:
        ret = chunkTrace(inputs[1], blockids, origin, libs, fn_args, object_number)
        return ret
    elif inputs[0] == 12:
        ret = getblock(idgen.getID(), "get_variable", [libs.get_var(inputs[2]), None])
        return ret
    else:
        #todo
        pass

def getblock(id, type, params, statement = []):
    block = {
        "id": id, "type": type,
        "x": 0, "y": 0,
        "movable": None,
        "deletable": 1,
        "emphasized": False,
        "readOnly": None,
        "copyable": True,
        "statements": statement,
        "extensions": [],
        "params": params
    }
    return block