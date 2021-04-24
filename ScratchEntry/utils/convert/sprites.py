import utils.idgen as idgen
import utils.convert.variables as variables

import PIL, json

def convert(origin: dict, libs):
    dict_items = []
    localvars = []
    localdatas = {}
    for i in origin:
        if i["isStage"] == True: continue
        ret = dict()

        ret["id"] = idgen.getID()
        ret["name"] = i["name"]
        
        #지역변수 처리
        vars, varids = variables.convert(i["variables"], target = ret["id"])
        lists, listids = variables.convert(i["lists"], target = ret["id"], isList = True)
        localvars += vars + lists
        localdatas = {**localdatas, **varids, **listids}

        ret["objectType"] = "sprite"
        ret["rotateMethod"] = "free"
        ret["scene"] = "qqqq"
        ret["lock"] = False
        ret["sprite"] = { "pictures": [] }
        for j in i["costumes"]:
            image = PIL.Image.open(f"temp/{j['md5ext'][0:2]}/{j['md5ext'][2:4]}/image/{j['assetId']}.png")
            width, height = image.size

            ret["sprite"]["pictures"].append({
                "id": idgen.getID(),
                "dimension": { "width": width, "height": height },
                "fileurl": f"temp/{j['md5ext'][0:2]}/{j['md5ext'][2:4]}/image/{j['md5ext']}",
                "name": j["assetId"],
                "filename": j["assetId"],
                "imageType": j["md5ext"][-3::1],
                "scale": 100
            })
        ret["selectedPictureId"] = ret["sprite"]["pictures"][i["currentCostume"]]["id"]

        ret["entity"] = {
            "font": "undefinedpx",
            "x": i["x"],
            "y": i["y"],
            "size": i["size"],
            "visible": i["visible"],
            "rotation": (i["direction"] + 270) % 360,
            "direction": 90,
            "width": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["width"],
            "height": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["height"],
            "regX": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["width"] / 2,
            "regY": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["height"] / 2,

            "scaleX": 1,
            "scaleY": 1,
        }

        print(f"Converted: Sprite '{i['name']}' to '{ret['id']}'")
        dict_items.append(ret)

    return dict_items, localvars, localdatas