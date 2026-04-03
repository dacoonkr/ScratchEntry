import BLL.bll as BLL
import BLL.util as UTIL

def s2b(json):
    out = BLL.BLLfile()
    id_gen = UTIL.short_ID_generator()
    id_map = dict()
    for cur in json["targets"]:
        #오브젝트 파싱
        obj = BLL.BLLobj()
        obj._id = id_gen.new_id()
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
            id_map[costume["assetId"]] = id_gen.new_id()
            src = BLL.BLLsrc()
            src._id = id_map[costume["assetId"]]
            src._type = "img"
            src._filepath = id_map[costume["assetId"]] + "." + costume["dataFormat"]
            src._center = [costume["rotationCenterX"], costume["rotationCenterY"]]
            obj._srcs.append(src._id)
            out._global_srcs.append(src)

        #소리 파싱
        for sound in cur["sounds"]:
            id_map[sound["assetId"]] = id_gen.new_id()
            src = BLL.BLLsrc()
            src._id = id_map[sound["assetId"]]
            src._type = "aud"
            src._filepath = id_map[sound["assetId"]] + "." + sound["dataFormat"]
            obj._srcs.append(src._id)
            out._global_srcs.append(src)

        #파생 변수 파싱
        for var_key in cur["variables"]:
            id_map[var_key] = id_gen.new_id()
            var = BLL.BLLvar()
            var._id = id_map[var_key]
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
            id_map[var_key] = id_gen.new_id()
            var = BLL.BLLvar()
            var._id = id_map[var_key]
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
            id_map[var_key] = id_gen.new_id()
            cast = BLL.BLLcast()
            cast._id = id_map[var_key]
            cast._displayname = cur["broadcasts"][var_key]
            out._casts.append(cast)

        #파생 블록 파싱

        out._objs.append(obj)

    return out, id_map