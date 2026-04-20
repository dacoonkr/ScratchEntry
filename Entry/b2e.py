import BLL.bll as BLL
import BLL.util as UTIL
import Entry.ent as ENT
import Filesystem.file as FS
import Entry.b2e_block as BLOCK
import Entry.translation as TRANS
import Entry.regis as REGIS
import json

def b2e(bll: BLL.BLLfile, input_path):
    out = ENT.ENTfile()
    var_pos_gen = UTIL.var_position_generator()
    trans: TRANS.translator = TRANS.translator()
    out._json["name"] = bll._name
    scene = bll._id_gen.new_id()
    out._json["scenes"] = [{
        "id": scene,
        "name": "Stage"
    }]
    pre_registrator = REGIS.pre_registrator(function_build, trans) #실행 전 레지스트레이션
    pre_registrator.mount(bll, out)
    registration_match = dict() #실행 후 레지스트레이션 obj_id:index
    for obj_i in bll._objs:
        obj, procedures = obj_build(bll, obj_i, scene, input_path)
        registration_match[obj_i._id] = len(out._json["objects"])
        out._json["objects"].append(obj)
        for procedure in procedures:
            out._json["functions"].append(function_build(bll, obj, procedure, trans))
    for cast in bll._casts:
        out._json["messages"].append(broadcast_build(bll, cast))
    for var in bll._vars:
        out._json["variables"].append(var_build(var_pos_gen, var))
    for regis in bll._registrations:
        out._json["objects"][registration_match[regis._target._id]]["script"].append(regis._snippet.build(bll, regis._target, regis._params, dict(), trans))
    out._json["interface"]["object"] = bll._objs[0]._id
    return out

def function_build(bll: BLL.BLLfile, obj: BLL.BLLobj, procedure: BLL.BLLprocedure, trans: TRANS.translator):
    out = dict()
    out["id"] = procedure[0]._id
    out["type"] = "normal"
    out["localVariables"] = []
    out["useLocalVariables"] = False
    param_block = None
    for i in procedure[0]._arguments[::-1]:
        type_str = "function_field_string" if i[0] == "s" else "function_field_boolean"
        type_param = "stringParam_" if i[0] == "s" else "booleanParam_"
        if i[1] in bll._procedure_var_map:
            param_block = trans.block_build(bll, obj, 0, 0, type_str, "", ["A", "B"], {
                "A": trans.block_build(bll, obj, 0, 0, type_param + bll._procedure_var_map[i[1]], "", [], dict()),
                "B": param_block
            })
    out["content"] = json.dumps([[trans.block_build(bll, obj, 0, 0, "function_create", "", ["A", "*B"], {
        "A": param_block,
        "B": procedure[1:]
    })]])
    return out

def broadcast_build(bll: BLL.BLLfile, cast: BLL.BLLcast):
    out = dict()
    out["id"] = cast._id
    out["name"] = cast._displayname
    return out

def obj_build(bll: BLL.BLLfile, obj: BLL.BLLobj, scene, input_path):
    out = dict()
    out["id"] = obj._id
    out["name"] = obj._displayname
    script, procedures = BLOCK.code_build(bll, obj, obj._codes)
    out["script"] = script #dump전으로 저장
    out["objectType"] = "sprite"
    out["rotateMethod"] = "free"
    out["scene"] = scene
    out["sprite"] = dict()
    out["sprite"]["pictures"] = []
    out["sprite"]["sounds"] = []
    for src_id in obj._srcs:
        src = obj._parent._global_srcs[src_id]
        if src._type == "img":
            out["sprite"]["pictures"].append(shape_build(src, input_path))
        if src._type == "aud":
            pass #오류로 인해 잠시 패스
            #out["sprite"]["sounds"].append(sound_build(src, input_path))
    sel_shape = out["sprite"]["pictures"][obj._shape_idx - 1]
    out["selectedPictureID"] = sel_shape["id"]
    out["lock"] = True
    out["entity"] = {
        "x": obj._position[0],
        "y": obj._position[1],
        "regX": sel_shape["dimension"]["width"] / 2,
        "regY": sel_shape["dimension"]["height"] / 2,
        "scaleX": obj._size_percent / 100,
        "scaleY": obj._size_percent / 100,
        "rotation": (obj._direction + 270) % 360,
        "direction": 90,
        "width": sel_shape["dimension"]["width"],
        "height": sel_shape["dimension"]["height"],
        "font": "undefinedpx ",
        "visible": obj._visible
    }
    return out, procedures

def shape_build(src: BLL.BLLsrc, input_path):
    out = dict()
    out["id"] = src._id
    out["dimension"] = dict()
    out["dimension"]["width"], out["dimension"]["height"] = FS.image_getsize(input_path, src._filepath)
    out["dimension"]["scaleX"] = 1
    out["dimension"]["scaleY"] = 1
    out["filename"] = src._id
    out["name"] = src._displayname
    out["imageType"] = src._filepath[-3:]
    out["fileurl"] = f'temp/{src._filepath[0:2]}/{src._filepath[2:4]}/image/{src._filepath}'
    return out

def sound_build(src: BLL.BLLsrc, input_path):
    out = dict()
    out["id"] = src._id
    out["name"] = src._displayname
    out["ext"] = src._filepath[-4:]
    out["fileurl"] = f'temp/{src._filepath[0:2]}/{src._filepath[2:4]}/sound/{src._filepath}'
    out["duration"] = FS.audio_getsize(input_path, src._filepath)
    return out

def var_build(pos_gen: UTIL.var_position_generator, var: BLL.BLLvar):
    out = dict()
    out["name"] = var._displayname
    out["id"] = var._id
    out["visible"] = False
    out["value"] = var._initial
    if var._type == "var":
        out["variableType"] = "variable"
        out["x"], out["y"] = pos_gen.new_var()
    elif var._type == "list":
        out["variableType"] = "list"
        out["x"], out["y"] = pos_gen.new_list()
        out["width"], out["height"] = 100, 120
    out["isCloud"] = var._online
    out["isRealTime"] = False
    out["cloudDate"] = False
    out["object"] = None if var._dependency == "" else var._dependency
    return out