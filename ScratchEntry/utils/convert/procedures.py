import utils.convert.blocks as blocks
import utils.idgen as idgen

import json

def convert(cur, origin, libs):
    source = cur
    cur = origin[cur]["inputs"]["custom_block"][1]

    args = json.loads(origin[cur]["mutation"]["argumentids"])
    names = json.loads(origin[cur]["mutation"]["argumentnames"])
    proccode = origin[cur]["mutation"]["proccode"]

    ret = blocks.getblock(libs.get_fn(args), "function_create", [])
    types = []

    while True:
        st = proccode.find("%s")
        bo = proccode.find("%b")
        if st == -1 and bo == -1: break

        s = list(proccode)
        if st == -1: 
            s[bo] = '$'
            types.append("boolean")
        elif bo == -1: 
            s[st] = '$'
            types.append("string")
        else:
            if min(st, bo) == st:
                types.append("boolean")
            else:
                types.append("string")
            s[min(st, bo)] = '$'

        proccode = "".join(s)

    block, arglists = subargs(args, types)
    ret["params"] = [block, None]

    fn_args = {}
    for x in range(len(args)):
        fn_args[names[x]] = arglists[x]
    
    blockids = {}
    for i in origin:
        blockids[i] = idgen.getID()
    
    b = blocks.chunkTrace(origin[source]["next"], blockids, origin, libs, fn_args = fn_args)
    if b == None: b = []
    return [ret] + b

def get_fn_definition(params):
    fn_definition = blocks.getblock(idgen.getID(), "function_create", [])

    block, arglists = subargs(params)
    fn_definition["params"] = [block, None]

    return fn_definition

def subargs(args, types):
    if len(args) == 0: return None, []
    fnParam, argblock = None, None
    sub, fn_args = subargs(args[1:], types[1:])
    if types[0] == "string":
        fnParam = blocks.getblock(idgen.getID(), f"stringParam_{idgen.getID()}", [])
        argblock = blocks.getblock(idgen.getID(), "function_field_string", [fnParam, sub])
    elif types[0] == "boolean":
        fnParam = blocks.getblock(idgen.getID(), f"booleanParam_{idgen.getID()}", [])
        argblock = blocks.getblock(idgen.getID(), "function_field_boolean", [fnParam, sub])
    return argblock, [fnParam["type"]] + fn_args