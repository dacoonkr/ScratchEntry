import IDgen

def initEntfile():
	ent: dict = {}

	ent["objects"] = []
	ent["scenes"] = [{"id": IDgen.getID(), "name": "stage"}]
	ent["variables"] = [{
      "name": "초시계",
      "id": "time",
      "visible": False,
      "value": "0",
      "variableType": "timer",
      "isCloud": False,
      "isRealTime": False,
      "cloudDate": False,
      "object": None,
      "x": 134,
      "y": -70
    }, {
      "name": "대답",
      "id": "answ",
      "visible": False,
      "value": "0",
      "variableType": "answer",
      "isCloud": False,
      "isRealTime": False,
      "cloudDate": False,
      "object": None,
      "x": 150,
      "y": -100
    }]
	ent["messages"] = []
	ent["functions"] = []
	ent["tables"] = []
	ent["interface"] = {
		"canvasWidth": 640,
		"menuWidth": 280,
		"object": "1111"
	}
	ent["expansionBlocks"] = []
	ent["aiUtilizeBlocks"] = []
	ent["externalModules"] = []

	ent["speed"] = 60
	ent["likeCnt"] = 0
	ent["recentLikeCnt"] = 0
	ent["childCnt"] = 0
	ent["comment"] = 0
	ent["visit"] = 0
	ent["name"] = "Generated by ScratchEntry Generator"
	ent["user"] = "5bc9c961a92d6f57fce93303"
	ent["isopen"] = False
	ent["isPracticalCourse"] = False

	return ent