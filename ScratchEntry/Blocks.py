import IDgen

def blocksParse(origin: dict):
    blockids = {}

    header = []

    for i in origin:
        blockids[i] = IDgen.getID()

        block = origin[i]
        if block["parent"] == None:
            header.append(i)

    ret = []
    for i in header:
        ret.append(chunkTrace(i, blockids, origin))

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
    "repeat_inf", "repeat_basic"
]

def chunkTrace(cur, blockids, origin):
    ret = []
    while True:
        try: opcode = reps[origin[cur]["opcode"]]
        except: pass
        else:
            if opcode == 0:
                ret.append(getblock(blockids[cur], rets[opcode], [None]))

            if opcode == 4:
                param = paramTrace(origin[cur]["inputs"]["DURATION"], blockids, origin);
                ret.append(getblock(blockids[cur], rets[opcode], [param, None]))

            #사칙 연산자
            if 14 <= opcode <= 17:
                param1 = paramTrace(origin[cur]["inputs"]["NUM1"], blockids, origin);
                param2 = paramTrace(origin[cur]["inputs"]["NUM2"], blockids, origin);
                mid = ["PLUS", "MINUS", "MULTI", "DIVIDE"][opcode - 14]

                ret.append(getblock(blockids[cur], rets[opcode], [param1, mid, param2, None]))

            #반복
            if opcode == 18 or opcode == 19:
                times = None
                if opcode == 19: 
                    times = paramTrace(origin[cur]["inputs"]["TIMES"], blockids, origin)
                substk = paramTrace(origin[cur]["inputs"]["SUBSTACK"], blockids, origin);
                ret.append(getblock(blockids[cur], rets[opcode], [times, None], statement = [substk]))
            
                print(f"Converted: Block '{cur}' to Block '{blockids[cur]}'")

        if origin[cur]["next"] == None: break
        cur = origin[cur]["next"]

    return ret

def paramTrace(inputs, blockids, origin):
    if inputs[0] == 1:
        return getblock(IDgen.getID(), "number", [inputs[1][1]])
    elif inputs[0] == 3:
        ret = chunkTrace(inputs[1], blockids, origin)
        return ret[0]
    elif inputs[0] == 2:
        ret = chunkTrace(inputs[1], blockids, origin)
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