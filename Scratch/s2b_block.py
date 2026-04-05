import BLL.bll as BLL

def code_search(id_gen, id_map, json, cur_id):
    blocks = BLL.BLLblocks()
    stat_cnt = 0
    while cur_id != None:
        block = BLL.BLLblock()
        block._id = id_gen.new_id()
        block._command = json[cur_id]["opcode"]
        if "mutation" in json[cur_id]: block._mutation = json[cur_id]["mutation"]
        for param in json[cur_id]["inputs"]:
            param_v = json[cur_id]["inputs"][param][1]
            if type(param_v) == str:
                #새 블럭이 있다 -> BLLblocks타입
                block._param[param], cnt = code_search(id_gen, id_map, json, param_v)
                stat_cnt += cnt
            elif param_v == None:
                pass
            else: #리터럴이 있다 -> 단일 BLLblock타입
                tmp = BLL.BLLblock()
                if param_v[0] == 12:
                    tmp.literal("var", param_v[1])
                elif param_v[0] == 13:
                    tmp.literal("list", param_v[1])
                else: tmp.literal("text", param_v[1])
                block._param[param] = tmp
        for field in json[cur_id]["fields"]:
            block._field[field] = json[cur_id]["fields"][field][0]
        blocks._blocks.append(block)
        stat_cnt += 1
        cur_id = json[cur_id]["next"]
    return blocks, stat_cnt