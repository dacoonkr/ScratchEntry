import utils.idgen as idgen
import utils.convert.procedures as procedures
import utils.convert.macro.macros as macros

import json

def convert(origin: dict, libs):
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
            functions.append([procedures.convert(i, origin, libs), 
                              origin[origin[i]["inputs"]["custom_block"][1]]["mutation"]["proccode"]])
        else:
            ret.append(chunkTrace(i, blockids, origin, libs, {}))

    return ret, functions

def chunkTrace(cur, blockids, origin, libs, fn_args):
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
                params.append(paramTrace(origin[cur]["inputs"][argid], blockids, origin, libs, fn_args))
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
                    elif x[0] == '!':
                        params.append(libs.get_brd(origin[cur]["inputs"]["BROADCAST_INPUT"][1][2]))
                    elif x[0] == '*':
                        params.append(libs.get_spt(origin[origin[cur]["inputs"][x[1:]][1]]["fields"][x[1:]][0]))
                    elif x == '&VARIABLE' or x == '&LIST':
                        params.append(libs.get_var(origin[cur]["fields"][x[1:]][1]))
                    elif x == '&NULL':
                        params.append(None)
                    else:
                        d = paramTrace(origin[cur]["inputs"][x], blockids, origin, libs, fn_args)
                        params.append(d)
                if found["type"] == "direct" or found["type"] == "operator" or found["type"] == "header":
                    if found["code"] == "boolean_not":
                        ret.append(getblock(blockids[cur], found["code"], params[1] + [None]))
                    ret.append(getblock(blockids[cur], found["code"], params + [None]))

                elif found["type"] == "substk":
                    if "SUBSTACK" in origin[cur]["inputs"]:
                        substk = paramTrace(origin[cur]["inputs"]["SUBSTACK"], blockids, origin, libs, fn_args)
                    else: substk = []

                    if found["code"] == "if_else" or found["code"] == "_if":
                        substk2 = None
                        if found["code"] == "if_else": 
                            substk2 = paramTrace(origin[cur]["inputs"]["SUBSTACK2"], blockids, origin, libs, fn_args)
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

def paramTrace(inputs, blockids, origin, libs, fn_args):
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
            ret = chunkTrace(inputs[1], blockids, origin, libs, fn_args)
            if len(ret) == 0: return []
            return ret[0]
    elif inputs[0] == 2:
        ret = chunkTrace(inputs[1], blockids, origin, libs, fn_args)
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