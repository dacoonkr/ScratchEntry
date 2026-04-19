class rule_from_bll:
    def __init__(self):
        self._type = ""
        self._params = []

class rule_to_ent:
    def __init__(self):
        self._type = ""
        self._commands = [] #list[list[str]]
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