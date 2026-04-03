class BLLfile:
    _name = ""
    _objs = [] #obj
    _global_srcs = [] #src
    _vars = [] #var
    _casts = [] #cast

class BLLobj:
    _id = ""
    _displayname = ""
    _shape_idx = 1 #1-base
    _srcs = [] #모양 src_id
    _order = 0 #보이는 순서
    _visible = True #숨기기,보이기
    _position = [0, 0]
    _size_percent = 100
    _direction = 90

class BLLsrc:
    _id = ""
    _type = "" #aud/img
    _filepath = ""
    _center = [0, 0] #todo, 회전중심이자, 좌표이동 시 중심 

class BLLvar:
    _id = ""
    _displayname = ""
    _type = "" #var/list
    _initial = "" #초기화값 number or str
    _online = False #온라인 연동 여부
    _dependency = "" #지역변수 obj_id / 빈 문자열 = global

class BLLcast:
    _id = ""
    _displayname = ""