import BLL.bll as BLL
import BLL.util as UTIL

class rule_from_bll:
    def __init__(self):
        self._type = ""
        self._params = []

class rule_to_ent:
    def __init__(self):
        self._type = ""
        self._params = [] #list[rule_to_ent, str]

def rule_from_bll_parse(s):
    li = s.strip("{}").split(':')
    out = rule_from_bll()
    out._type = li[0]
    out._params = li[1:]
    return out

def rule_to_ent_parse(s):
    s = s[1:len(s) - 1] + ":"
    li = []
    depth, cur = 0, ""
    for ch in s:
        if ch == '{' or ch == '[': depth += 1
        if ch == '}' or ch == ']': depth -= 1
        if ch == ':' and depth == 0:
            if cur.startswith("{"):
                li.append(rule_to_ent_parse(cur))
            else: li.append(cur)
            cur = ""
        else: cur += ch
    out = rule_to_ent()
    out._type = li[0]
    out._params = li[1:]
    return out

class translator:
    def __init__(self):
        self.rules = dict() # bll_type:[bll_rule, ent_rule]

        text = open("Entry/dict.txt", "r", encoding = "UTF-8").read()
        key_parsed, key = False, None

        for rule in text.split('\n'):
            if rule.startswith("#"): continue
            if rule.startswith("{"):
                if key_parsed:
                    self.rules[key._type] = [key, rule_to_ent_parse(rule)]
                    key_parsed = False
                else:
                    key_parsed, key = True, rule_from_bll_parse(rule)

    def format(self, text, bll: BLL.BLLfile, obj: BLL.BLLobj, format_rule):
        out = text
        for i in format_rule.strip('[]').split(','):
            if i == "%o":
                if out == "_stage_": out = "Stage"
                out = bll.find_obj(out)._id
            elif i == "%k":
                if out == "left arrow": out = "37"
                elif out == "up arrow": out = "38"
                elif out == "right arrow": out = "39"
                elif out == "down arrow": out = "40"
                elif out == "space": out = "32"
                else: out = str(ord(out.upper()))
            elif i == "%b":
                out = bll.find_cast(out)._id
            elif i == "%B":
                src = bll.find_obj("Stage").find_src(out)
                out = bll.find_cast(f"scene_changeto_{src._id}")._id
            elif i == "%c":
                out = obj.find_src(out)._id
            elif i == "%v":
                out = bll.find_var("var", out)._id
            elif i == "%l":
                out = bll.find_var("list", out)._id
            elif len(i) == 0: pass
            else:
                bef, aft = i.split(':')
                if out == bef:
                    out = aft
                    break
        return out

    def translation(self, bll: BLL.BLLfile, obj: BLL.BLLobj, x, y, block: BLL.BLLblock):
        if block._is_literal:
            if block._literal_mode == "text":
                return self.block_build(bll, obj, x, y, "text", block._literal_value, [], dict())
            if block._literal_mode == "var":
                return self.block_build(bll, obj, x, y, "get_variable", block._literal_value, [], dict())
            if block._literal_mode == "list": #구현 예정
                return self.block_build(bll, obj, x, y, "text", "", [], dict())
                pass
        if block._command == "argument_reporter_string_number" or block._command == "argument_reporter_boolean": #함수 인자 값
            value = block._field["VALUE"]
            if value not in bll._procedure_var_map:
                bll._procedure_var_map[value] = bll._id_gen.new_id()
            type_param = "stringParam_" if block._command[18] == "s" else "booleanParam_"
            return self.block_build(bll, obj, 0, 0, type_param + bll._procedure_var_map[value], "", [], dict())
        if block._command == "procedures_call": #함수 호출
            value = f"{obj._id}:{block._mutation['proccode']}"
            if value not in bll._procedures_map:
                bll._procedures_map[value] = bll._id_gen.new_id()
            params, in_param = [], dict()
            cnt = 0
            for param in block._param:
                params.append(cnt)
                if type(block._param[param]) == BLL.BLLblock: #리터럴
                    in_param[cnt] = block._param[param] #BLLblock
                if type(block._param[param]) == BLL.BLLblocks: #단일블럭
                    in_param[cnt] = block._param[param]._blocks[0] #BLLblock
                cnt += 1
            return self.block_build(bll, obj, x, y, f"func_{bll._procedures_map[value]}", 0, params, in_param)
            
        if not block._command in self.rules:
            print("Missing Definition:", block._command)
            return self.block_build(bll, obj, x, y, "show", 0, [], dict())
        rule, in_param = self.rules[block._command], dict() #key:
        for param in rule[0]._params:
            print(obj._displayname, block._command)
            if param.startswith("@@"):
                param = param[2:]
                in_param[param] = block._param[param]._literal_value #str
            elif param.startswith("@"):
                param = param[1:]
                in_param[param] = block._param[param]._blocks[0]._field[param] #str
            elif param.startswith("&"):
                param = param[1:]
                in_param[param] = block._field[param] #str
            elif param.startswith("*"): #STATEMENT
                param = param[1:]
                out = []
                if param in block._param:
                    for cur in block._param[param]._blocks: #BLLblock
                        out.append(self.translation(bll, obj, 0, 0, cur))
                in_param[param] = out
            elif type(block._param[param]) == BLL.BLLblock: #리터럴
                if param not in block._param: #빈칸, 대부분 미완성 코드이므로 중요치 않음
                    in_param[param] = "0"
                else: in_param[param] = block._param[param] #BLLblock
            elif type(block._param[param]) == BLL.BLLblocks: #단일블럭
                in_param[param] = block._param[param]._blocks[0] #BLLblock
                
        out = self.block_build(bll, obj, x, y, rule[1]._type, 0, rule[1]._params, in_param)
        return out

    def block_build(self, bll: BLL.BLLfile, obj, x, y, command, literal_value, params, in_param: dict):
        out = dict()
        out["id"] = bll._id_gen.new_id()
        out["movable"] = None
        out["deletable"] = 1
        out["emphasized"] = False
        out["readOnly"] = None
        out["copyable"] = True
        out["assemble"] = True
        out["extensions"] = []
        out["x"], out["y"] = x, y
        out["params"] = []
        out["statements"] = []
        out["type"] = command
        if command == "text":
            out["params"] = [str(literal_value)]
            return out
        if command == "get_variable":
            out["params"] = [bll.find_var("var", literal_value)._id]
            return out
        for param in params:
            if type(param) == str:
                if param.startswith("*"): #statement
                    out["statements"].append(in_param[param[1:]])
                    continue

                child = None
                format_rule = "[]"
                if "%" in param:
                    format_rule = param[param.find('%') + 1:]
                    param = param[:param.find('%')]
                if param == "&!": pass
                elif param.startswith("&&"):
                    child = self.block_build(bll, obj, 0, 0, "text", param[2:], [], dict())
                elif param.startswith("&"):
                    child = param[1:]
                elif param.startswith("@"):
                    child = self.format(in_param[param[1:]], bll, obj, format_rule)
                elif param.startswith("?"):
                    if param == "?b":
                        child = bll.find_obj("Stage")._id
                    elif param == "?B":
                        child = bll.find_cast(f"scene_changenext")._id
                else:
                    if type(in_param[param]) == dict:
                        child = in_param[param]
                    elif type(in_param[param]) == BLL.BLLblock:
                        child = self.translation(bll, obj, 0, 0, in_param[param])
                out["params"].append(child)

            elif type(param) == rule_to_ent:
                out["params"].append(self.block_build(bll, obj, 0, 0, param._type, 0, param._params, in_param))
        return out