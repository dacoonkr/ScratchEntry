import utils.idgen as idgen

def convert(origin: dict, libs):
    blockids = {}

    header = []

    for i in origin:
        blockids[i] = idgen.getID()

        block = origin[i]
        try:
            if block["parent"] == None:
                header.append(i)
        except: pass

    ret = []
    for i in header:
        ret.append(chunkTrace(i, blockids, origin, libs))

    return ret

reps = {
    "event_whenflagclicked": 0,
    "event_whenkeypressed": 1,
    "event_whenthisspriteclicked": 2,
    "event_whenbroadcastreceived": 3,
    "control_wait": 4,
    "control_repeat": 5,
    "control_forever": 6,
    "control_if": 7,
    "control_if_else": 8,
    "control_wait_until": 9,
    "control_repeat_until": 10,
    "control_start_as_clone": 11,
    "control_create_clone_of": 12,
    "control_delete_this_clone": 13,

    "operator_add": 14, "operator_subtract": 15, 
    "operator_multiply": 16, "operator_divide": 17,

    "control_forever": 18, "control_repeat": 19,
}

rets = [
    "when_run_button_click",
    "when_some_key_pressed",
    "when_object_click",
    "when_message_cast",
    "wait_second",
    "repeat_basic",
    "repeat_inf",
    "_if",
    "if_else",
    "wait_until_true",
    "repeat_while_true",
    "when_clone_start",
    "create_clone",
    "delete_clone",

    #사칙연산자
    "calc_basic", "calc_basic", "calc_basic", "calc_basic",

    #반복
    "repeat_inf", "repeat_basic",
]

def chunkTrace(cur, blockids, origin, libs):
    ret = []
    while True:
        found = libs.find(origin[cur]["opcode"])
        if found != None:
            if found["type"] == "direct":
                params = []
                for x in found["params"]:
                    params.append(paramTrace(origin[cur]["inputs"][x], blockids, origin, libs))
                ret.append(getblock(blockids[cur], found["code"], params + [None]))
        else:
            try: opcode = reps[origin[cur]["opcode"]]
            except: pass
            else:
                if opcode == 0:
                    ret.append(getblock(blockids[cur], rets[opcode], [None]))

                if opcode == 4:
                    param = paramTrace(origin[cur]["inputs"]["DURATION"], blockids, origin, libs)
                    ret.append(getblock(blockids[cur], rets[opcode], [param, None]))

                #사칙 연산자
                if 14 <= opcode <= 17:
                    param1 = paramTrace(origin[cur]["inputs"]["NUM1"], blockids, origin, libs)
                    param2 = paramTrace(origin[cur]["inputs"]["NUM2"], blockids, origin, libs)
                    mid = ["PLUS", "MINUS", "MULTI", "DIVIDE"][opcode - 14]

                    ret.append(getblock(blockids[cur], rets[opcode], [param1, mid, param2, None]))

                #반복
                if opcode == 18 or opcode == 19:
                    times = None
                    if opcode == 19: 
                        times = paramTrace(origin[cur]["inputs"]["TIMES"], blockids, origin, libs)
                    substk = paramTrace(origin[cur]["inputs"]["SUBSTACK"], blockids, origin, libs)
                    ret.append(getblock(blockids[cur], rets[opcode], [times, None], statement = [substk]))
                
                    print(f"Converted: Block '{cur}' to '{blockids[cur]}'")

                #좌표 이동
                if opcode == 20 or opcode == 21:
                    param1 = paramTrace(origin[cur]["inputs"]["X"], blockids, origin, libs)
                    param2 = paramTrace(origin[cur]["inputs"]["Y"], blockids, origin, libs)
                    if opcode == 21:
                        sec = paramTrace(origin[cur]["inputs"]["SECS"], blockids, origin, libs)
                        ret.append(getblock(blockids[cur], rets[opcode], [sec, param1, param2, None]))
                    else:
                        ret.append(getblock(blockids[cur], rets[opcode], [param1, param2, None]))
                if 22 <= opcode <= 25:
                    param = paramTrace(origin[cur]["inputs"][["DX", "X", "DY", "Y"][opcode - 22]], blockids, origin, libs)
                    ret.append(getblock(blockids[cur], rets[opcode], [param, None]))

        if origin[cur]["next"] == None: break
        cur = origin[cur]["next"]

    return ret

def paramTrace(inputs, blockids, origin, libs):
    if inputs[0] == 1:
        return getblock(idgen.getID(), "number", [inputs[1][1]])
    elif inputs[0] == 3:
        ret = chunkTrace(inputs[1], blockids, origin, libs)
        return ret[0]
    elif inputs[0] == 2:
        ret = chunkTrace(inputs[1], blockids, origin, libs)
        return ret
    else:
        #todo
        pass

def getblock(id, type, params, statement = []):
    block = {
        "id": id, "type": type,
        "x": 0, "y": 0, "statements": [],
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