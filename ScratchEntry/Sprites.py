import IDgen

def spritesParse(origin: dict):
	dict_items = []
	for i in origin:
		if i["isStage"] == True: continue
		ret = dict()

		ret["id"] = IDgen.get_id()
		ret["name"] = i["name"]

		ret["objectType"] = "sprite"
		ret["rotateMethod"] = "free"
		ret["script"] = "[]"
		ret["scene"] = "qqqq"
		ret["lock"] = False
		ret["sprite"] = { "pictures": [] }
		for j in i["costumes"]:
			ret["sprite"]["pictures"].append({
                "id": IDgen.get_id(),
                "dimension": { "width": 100, "height": 100 },
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
            "rotation": i["direction"],
            "direction": 90,
            "width": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["width"],
            "height": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["height"],
            "regX": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["width"] / 2,
            "regY": ret["sprite"]["pictures"][i["currentCostume"]]["dimension"]["height"] / 2,

            "scaleX": 0.3154574132492113,
            "scaleY": 0.3154574132492113,
        }

		dict_items.append(ret)
	return dict_items