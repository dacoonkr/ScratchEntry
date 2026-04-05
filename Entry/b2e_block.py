import BLL.bll as BLL
import BLL.util as UTIL
import Entry.translation as TRANS
import json

def code_build(bll: BLL.BLLfile, obj: BLL.BLLobj, code: list[BLL.BLLblocks]):
    trans = TRANS.translator()
    block_pos_gen = UTIL.block_position_generator()
    out, procedure_out = [], []
    for blocks in code:
        cur = []
        if blocks._blocks[0]._command == "procedures_definition":
            #[procedure, block...]
            cur.append(parse_procedure(bll, obj, blocks._blocks[0]))
            for block in blocks._blocks[1:]:
                cur.append(trans.translation(bll, obj, 0, 0, block))
            procedure_out.append(cur)
        else:
            x, y = block_pos_gen.new_block()
            for block in blocks._blocks: #block: BLL.BLLblock
                cur.append(trans.translation(bll, obj, x, y, block))
            out.append(cur)

    #배경에게 신호받고 전환 코드 첨가
    if obj._displayname == "Stage":
        for key in obj._srcs:
            src = obj._parent._global_srcs[key]
            x, y = block_pos_gen.new_block()
            if src._type == "img":
                out.append([
                    trans.block_build(bll, obj, x, y, "when_message_cast", "", ["&!", "@tmp"], {
                        "tmp": bll.find_cast(f"scene_changeto_{src._id}")._id
                    }),
                    trans.block_build(bll, obj, x, y, "change_to_some_shape", "", ["@tmp"], {
                        "tmp": src._displayname
                    }),
                ])
    return out, procedure_out

def parse_procedure(bll: BLL.BLLfile, obj: BLL.BLLobj, definition: BLL.BLLblock):
    mutation = definition._param["custom_block"]._blocks[0]._mutation
    value = f"{obj._id}:{mutation['proccode']}"
    if value not in bll._procedures_map:
        bll._procedures_map[value] = bll._id_gen.new_id()
    procedure = BLL.BLLprocedure()
    procedure._id = bll._procedures_map[value]
    procedure._dependency = obj._id
    argument_names = json.loads(mutation["argumentnames"])
    cnt = 0
    for i in range(len(mutation["proccode"])):
        if mutation["proccode"][i] == "%":
            procedure._arguments.append([mutation["proccode"][i + 1], argument_names[cnt]])
            cnt += 1
    return procedure