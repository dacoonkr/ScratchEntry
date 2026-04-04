import BLL.bll as BLL
import BLL.util as UTIL
import Entry.translation as TRANS

def code_build(bll: BLL.BLLfile, code: list[BLL.BLLblocks]):
    trans = TRANS.translator()
    block_pos_gen = UTIL.block_position_generator()
    out = []
    for blocks in code:
        cur = []
        for block in blocks._blocks: #block: BLL.BLLblock
            x, y = block_pos_gen.new_block()
            cur.append(trans.translation(bll, x, y, block))
        out.append(cur)
    return out