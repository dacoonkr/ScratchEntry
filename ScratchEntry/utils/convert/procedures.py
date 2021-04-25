import utils.convert.blocks as blocks
import utils.idgen as idgen

import json

def convert(cur, origin, libs):
    source = cur
    cur = origin[cur]["inputs"]["custom_block"][1]

    args = json.loads(origin[cur]["mutation"]["argumentids"])
    names = json.loads(origin[cur]["mutation"]["argumentnames"])

    ret = blocks.getblock(libs.get_fn(args), "function_create", [])

    block, arglists = subargs(args)
    ret["params"] = [block, None]

    fn_args = {}
    for x in range(len(args)):
        fn_args[names[x]] = arglists[x]
    
    blockids = {}
    for i in origin:
        blockids[i] = idgen.getID()
    return [ret] + blocks.chunkTrace(origin[source]["next"], blockids, origin, libs, fn_args = fn_args)

def get_fn_definition(params):
    fn_definition = blocks.getblock(idgen.getID(), "function_create", [])

    block, arglists = subargs(params)
    fn_definition["params"] = [block, None]

    return fn_definition

def subargs(args):
    if len(args) == 0: return None, []
    stringParam = blocks.getblock(idgen.getID(), f"stringParam_{idgen.getID()}", [])
    sub, fn_args = subargs(args[1:])
    argblock = blocks.getblock(idgen.getID(), "function_field_string", [stringParam, sub])
    return argblock, [stringParam["type"]] + fn_args