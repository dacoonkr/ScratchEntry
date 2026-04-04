import BLL.bll as BLL
import BLL.util as UTIL
import Entry.ent as ENT
import Filesystem.file as FS
import Entry.b2e_block as BLOCK
import json

def b2e(bll: BLL.BLLfile, input_path):
    out = ENT.ENTfile()
    var_pos_gen = UTIL.var_position_generator()
    out._json["name"] = bll._name
    scene = bll._id_gen.new_id()
    out._json["scenes"] = [{
        "id": scene,
        "name": "Stage"
    }]
    for var in bll._vars:
        out._json["variables"].append(var_build(var_pos_gen, var))
    for obj in bll._objs:
        out._json["objects"].append(obj_build(bll, obj, scene, input_path))
    for cast in bll._casts:
        out._json["messages"].append(broadcast_build(bll, cast))
    out._json["interface"]["object"] = bll._objs[0]._id
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
    out["script"] = json.dumps(BLOCK.code_build(bll, obj, obj._codes))
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
    return out

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