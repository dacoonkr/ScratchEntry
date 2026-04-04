import BLL.bll as BLL
import BLL.util as UTIL
import Entry.translation as TRANS

def code_build(bll: BLL.BLLfile, obj: BLL.BLLobj, code: list[BLL.BLLblocks]):
    trans = TRANS.translator()
    block_pos_gen = UTIL.block_position_generator()
    out = []
    for blocks in code:
        cur = []
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
    return out