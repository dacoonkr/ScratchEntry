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

    def format(self, text, bll: BLL.BLLfile, format_rule):
        out = text
        for i in format_rule.strip('[]').split(','):
            if i == "%o":
                out = bll.find_obj(out)._id
            else:
                bef, aft = i.split(':')
                if out == bef:
                    out = aft
                    break
        return out

    def translation(self, bll: BLL.BLLfile, x, y, block: BLL.BLLblock):
        if block._is_literal:
            return self.block_build(bll, x, y, "text", block._literal_value, [], dict())
        rule, in_param = self.rules[block._command], dict() #key:
        for param in rule[0]._params:
            if param.startswith("@"):
                param = param[1:]
                in_param[param] = block._param[param]._blocks[0]._field[param] #str
            elif param.startswith("*"): #STATEMENT
                param = param[1:] #작업 예정
            elif type(block._param[param]) == BLL.BLLblock: #리터럴
                in_param[param] = block._param[param] #BLLblock
            elif type(block._param[param]) == BLL.BLLblocks: #단일블럭
                in_param[param] = block._param[param]._blocks[0] #BLLblock
                
        out = self.block_build(bll, x, y, rule[1]._type, 0, rule[1]._params, in_param)
        return out

    def block_build(self, bll: BLL.BLLfile, x, y, command, literal_value, params, in_param: dict):
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
        for param in params:
            if type(param) == str:
                child = None
                format_rule = "[]"
                if "%" in param:
                    format_rule = param[param.find('%') + 1:]
                    param = param[:param.find('%')]
                if param == "&!": pass
                elif param.startswith("&&"):
                    child = self.block_build(bll, 0, 0, "text", param[2:], [], dict())
                elif param.startswith("&"):
                    child = param[1:]
                elif param.startswith("@"):
                    child = self.format(in_param[param[1:]], bll, format_rule)
                else: #statement
                    child = self.translation(bll, 0, 0, in_param[param])
                out["params"].append(child)
            elif type(param) == rule_to_ent:
                out["params"].append(self.block_build(bll, 0, 0, param._type, 0, param._params, in_param))
        return out