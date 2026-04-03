import BLL.bll as BLL

def code_search(id_gen, id_map, json, cur_id):
    blocks = BLL.BLLblocks()
    while cur_id != None:
        block = BLL.BLLblock()
        block._id = id_gen.new_id()
        block._command = json[cur_id]["opcode"]
        for param in json[cur_id]["inputs"]:
            param_v = json[cur_id]["inputs"][param][1]
            if type(param_v) == str:
                #새 블럭이 있다 -> BLLblocks타입
                block._param[param] = code_search(id_gen, id_map, json, param_v)
            else: #리터럴이 있다 -> 단일 BLLblock타입
                tmp = BLL.BLLblock()
                tmp.literal(param_v[1])
                block._param[param] = tmp
        blocks._blocks.append(block)
        cur_id = json[cur_id]["next"]
    return blocks