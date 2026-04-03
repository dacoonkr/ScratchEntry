import BLL.bll as BLL
import BLL.util as UTIL
import Scratch.s2b_block as BLOCK

def s2b(json):
    id_gen = UTIL.short_ID_generator()
    out = BLL.BLLfile(id_gen)
    id_map = dict()
    objs_map = dict()
    for cur in json["targets"]:
        #오브젝트 파싱
        obj = BLL.BLLobj(out)
        obj._id = objs_map[cur["name"]] = id_gen.new_id()
        obj._displayname = cur["name"]
        obj._shape_idx = cur["currentCostume"]
        obj._order = cur["layerOrder"]
        if not cur["isStage"]:
            obj._visible = cur["visible"]
            obj._position = [cur["x"], cur["y"]]
            obj._size_percent = cur["size"]
            obj._direction = cur["direction"]
        
        #모양 파싱
        for costume in cur["costumes"]:
            src = BLL.BLLsrc()
            src._id = id_map[costume["assetId"]] = id_gen.new_id()
            src._displayname = costume["name"]
            src._type = "img"
            src._filepath = id_map[costume["assetId"]] + "." + costume["dataFormat"]
            src._center = [costume["rotationCenterX"], costume["rotationCenterY"]]
            obj._srcs.append(src._id)
            out._global_srcs[src._id] = src

        #소리 파싱
        for sound in cur["sounds"]:
            src = BLL.BLLsrc()
            src._id = id_map[sound["assetId"]] = id_gen.new_id()
            src._displayname = sound["name"]
            src._type = "aud"
            src._filepath = id_map[sound["assetId"]] + "." + sound["dataFormat"]
            obj._srcs.append(src._id)
            out._global_srcs[src._id] = src

        #파생 변수 파싱
        for var_key in cur["variables"]:
            var = BLL.BLLvar()
            var._id = id_map[var_key] = id_gen.new_id()
            var._displayname = cur["variables"][var_key][0]
            var._type = "var"
            var._initial = cur["variables"][var_key][1]
            if cur["isStage"]: var._dependency = ""
            else: var._dependency = obj._id
            if len(cur["variables"][var_key]) > 2:
                var._online = cur["variables"][var_key][2]
            out._vars.append(var)
            
        #파생 리스트 파싱
        for var_key in cur["lists"]:
            var = BLL.BLLvar()
            var._id = id_map[var_key] = id_gen.new_id()
            var._displayname = cur["lists"][var_key][0]
            var._type = "list"
            var._initial = cur["lists"][var_key][1]
            if cur["isStage"]: var._dependency = ""
            else: var._dependency = obj._id
            if len(cur["lists"][var_key]) > 2:
                var._online = cur["lists"][var_key][2]
            out._vars.append(var)

        #파생 신호 파싱
        for var_key in cur["broadcasts"]:
            cast = BLL.BLLcast()
            cast._id = id_map[var_key] = id_gen.new_id()
            cast._displayname = cur["broadcasts"][var_key]
            out._casts.append(cast)

        out._objs.append(obj)

    for cur in json["targets"]:
        #파생 블록 파싱
        for block in cur["blocks"]:
            if cur["blocks"][block]["topLevel"]:
                blocks, stat_cnt = BLOCK.code_search(id_gen, id_map, cur["blocks"], block)
                out._stat_block_cnt += stat_cnt
                out.find_obj(cur["name"])._codes.append(blocks)
            
    return out, id_map