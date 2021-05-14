import utils.convert.blocks as blocks
import utils.idgen as idgen

import json

def convert(cur, origin, libs):
    source = cur
    cur = origin[cur]["inputs"]["custom_block"][1]

    args = json.loads(origin[cur]["mutation"]["argumentids"])
    names = json.loads(origin[cur]["mutation"]["argumentnames"])
    proccode = origin[cur]["mutation"]["proccode"]

    ret = blocks.getblock(libs.get_fn(proccode), "function_create", [])
    types = []

    if cur == 'wWtIT8Ezrhg*UgIdZ,)%':
        print(cur)

    while True:
        st = proccode.find("%s")
        nu = proccode.find("%n")
        bo = proccode.find("%b")
        if st == -1 and bo == -1 and nu == -1: break
        if st == -1: st = 999999999999999
        if bo == -1: bo = 999999999999999
        if nu == -1: nu = 999999999999999

        s = list(proccode)
        t = min(st, bo, nu)

        s[t] = ' '
        if s[t + 1] == 'n' or s[t + 1] == 's':
            types.append("string")
        elif s[t + 1] == 'b':
            types.append("boolean")

        proccode = "".join(s)

    block, arglists = subargs([proccode] + args, ["label"] + types)
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

def get_fn_definition(params, types):
    fn_definition = blocks.getblock(idgen.getID(), "function_create", [])

    block, arglists = subargs(params, types)
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
    elif types[0] == "label":
        fnParam = {"type": None}
        argblock = blocks.getblock(idgen.getID(), "function_field_label", [args[0], sub])
    return argblock, [fnParam["type"]] + fn_args