import IDgen, Blocks
import PIL, json

def spritesParse(origin: dict):
    dict_items = []
    for i in origin:
        if i["isStage"] == True: continue
        ret = dict()

        ret["id"] = IDgen.getID()
        ret["name"] = i["name"]

        ret["objectType"] = "sprite"
        ret["rotateMethod"] = "free"
        ret["script"] = json.dumps(Blocks.blocksParse(i["blocks"]))
        ret["scene"] = "qqqq"
        ret["lock"] = False
        ret["sprite"] = { "pictures": [] }
        for j in i["costumes"]:
            image = PIL.Image.open(f"temp/{j['md5ext'][0:2]}/{j['md5ext'][2:4]}/image/{j['assetId']}.png")
            width, height = image.size

            ret["sprite"]["pictures"].append({
                "id": IDgen.getID(),
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

        print(f"Converted: Sprite '{i['name']}' to Object '{ret['id']}'")
        dict_items.append(ret)
    return dict_items