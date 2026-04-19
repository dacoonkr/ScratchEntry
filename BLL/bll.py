class BLLfile:
    def __init__(self, id_gen):
        self._name = ""
        self._objs = [] #obj
        self._global_srcs = {} #id:src
        self._vars = [] #var
        self._casts = [] #cast
        self._procedures_map = {} #obj:proccode : procedure_id
        self._procedure_var_map = {} #name, id
        self._id_gen = id_gen
        self._stat_block_cnt = 0
        self._registrations = [] #BLLregistration
        
    def find_obj(self, displayname):
        for i in self._objs:
            if i._displayname == displayname:
                return i

    def find_cast(self, displayname):
        for i in self._casts:
            if i._displayname.lower() == displayname.lower():
                return i

    def find_var(self, mode, displayname):
        for i in self._vars:
            if i._type == mode and i._displayname == displayname:
                return i

class BLLobj:
    def __init__(self, bll):
        self._parent: BLLfile = bll
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
        
    def find_src(self, displayname):
        for i in self._srcs:
            if self._parent._global_srcs[i]._displayname == displayname:
                return self._parent._global_srcs[i]

class BLLblocks:
    def __init__(self):
        self._blocks = [] #list[BBLblock]

class BLLblock:
    def __init__(self):
        self._id = ""

        self._is_literal = False
        self._literal_mode = "text" #text,var,list
        self._literal_value = ""

        self._command = ""
        self._param = dict() #key: BLLblock or BLLblocks
        self._field = dict() #key:str
        self._mutation = dict() #함수 정의 전용

    def literal(self, mode, value):
        self._is_literal = True
        self._literal_mode = mode
        self._literal_value = value

class BLLsrc:
    def __init__(self):
        self._id = ""
        self._displayname = ""
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

class BLLprocedure:
    def __init__(self):
        self._id = ""
        self._dependency = "" #obj id
        self._arguments = [] # list[type, name] #s, b

class BLLregistration:
    def __init__(self):
        self._type = "" #chunk, func
        self._target = None #BLLobj
        self._params = {}
        self._snippet = None #snippet