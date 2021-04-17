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

    "event_broadcast": "",
    "event_broadcastandwait": "",
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
]

def chunkTrace(cur, blockids, origin):
    ret = []
    while True:
        print(cur)

        try: opcode = reps[origin[cur]["opcode"]]
        except: pass
        else:
            if opcode == 0:
                ret.append(getblock(blockids[cur], rets[opcode], [None]))
            if opcode == 4:
                dur = origin[cur]["inputs"]["DURATION"];
                if dur[0] == 1:
                    param1 = getblock(IDgen.getID(), "number", [dur[1][1]])

                ret.append(getblock(blockids[cur], rets[opcode], [param1, None]))

        if origin[cur]["next"] == None: break
        cur = origin[cur]["next"]

    return ret

def getblock(id, type, params):
    block = {
        "id": id, "type": type,
        "x": 0, "y": 0, "statements": [],
        "movable": None,
        "deletable": 1,
        "emphasized": False,
        "readOnly": None,
        "copyable": True,
        "extensions": [],
        "params": params
    }
    return block