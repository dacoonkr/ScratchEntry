class BLLfile:
    def __init__(self):
        self._name = ""
        self._objs = [] #obj
        self._global_srcs = [] #src
        self._vars = [] #var
        self._casts = [] #cast
    def find_obj(self, displayname):
        for i in self._objs:
            if i._displayname == displayname:
                return i

class BLLobj:
    def __init__(self):
        self._id = ""
        self._displayname = ""
        self._shape_idx = 1 #1-base
        self._srcs = [] #모양 src_id
        self._order = 0 #보이는 순서
        self._visible = True #숨기기,보이기
        self._position = [0, 0]
        self._size_percent = 100
        self._direction = 90
        self._codes = [] #list[BBLblocks]

class BLLblocks:
    def __init__(self):
        self._blocks = [] #list[BBLblock]

class BLLblock:
    def __init__(self):
        self._id = ""

        self._is_literal = False
        self._literal_value = ""

        self._command = ""
        self._param = dict() #값, statement포함
        self._field = dict() #선택

    def literal(self, value):
        self._is_literal = True
        self._literal_value = value

class BLLsrc:
    def __init__(self):
        self._id = ""
        self._type = "" #aud/img
        self._filepath = ""
        self._center = [0, 0] #todo, 회전중심이자, 좌표이동 시 중심 

class BLLvar:
    def __init__(self):
        self._id = ""
        self._displayname = ""
        self._type = "" #var/list
        self._initial = "" #초기화값 number or str
        self._online = False #온라인 연동 여부
        self._dependency = "" #지역변수 obj_id / 빈 문자열 = global

class BLLcast:
    def __init__(self):
        self._id = ""
        self._displayname = ""