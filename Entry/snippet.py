import BLL.bll as BLL
import Entry.snippet_dict as DICT
import Entry.rule as RULE

class snippet:
    def __init__(self):
        self._type = ""
        self._id = ""
        self._params = []
        self._commands = [] #list[list[str]]
        self._wrapper = None
        self._blocks = [] #list[rule_to_ent]

    #in_param(재귀적으로 전달)과 params(새로 입력)를 결합함
    def build(self, bll: BLL.BLLfile, obj: BLL.BLLobj, params: list, in_param: dict, trans) -> list:
        out = []
        for i in range(len(self._params)):
            in_param[self._params[i]] = params[i]

        skip = [False] * len(self._commands)
        for i in range(len(self._commands)):
            if skip[i]: continue
            command = self._commands[i]
            if command[0] == "vareach":
                for item in self.listup(bll, command[4]):
                    if command[2] == "lit":
                        literal = trans.block_build(bll, obj, 0, 0, "text", item, [], dict())
                        in_param[command[1]] = literal
                    if command[2] == "str":
                        in_param[command[1]] = item
                    for j in range(int(command[3])):
                        self.run_command(bll, obj, out, self._commands[i + 1 + j], in_param, trans)
                        skip[i + 1 + j] = True
            else:
                self.run_command(bll, obj, out, command, in_param, trans)

        return out

    def listup(self, bll: BLL.BLLfile, param):
        if param == "%o":
            return [i._displayname for i in bll._objs]
        elif param == "%b":
            return [i._displayname for i in bll._casts if not i._displayname.startswith("scene_")]
        elif param.startswith("["):
            return param.strip('[]').split(',')
        else: return []

    def run_command(self, bll: BLL.BLLfile, obj: BLL.BLLobj, out, command, in_param, trans):
        if command[0] == "sub":
            in_param[command[1]] = self._wrapper._definitions[command[2]].build(bll, obj, [], in_param, trans)
        if command[0] == "var":
            if command[2] == "lit":
                literal = trans.block_build(bll, obj, 0, 0, "text", command[3], [], dict())
                in_param[command[1]] = literal
            if command[2] == "str":
                in_param[command[1]] = command[3]
        if command[0] == "run":
            rule = self._blocks[command[1]]
            out.append(trans.block_build(bll, obj, 0, 0, rule._type, "", rule._params, in_param))

class snippet_wrapper:
    def __init__(self):
        self._definitions = dict() #id:<snippet>
        
        cur = snippet()
        for rule in DICT.snippet_text.split('\n'):
            rule = rule.strip()
            if len(rule) == 0 or rule.startswith("#"): continue
            elif rule == "end":
                self._definitions[cur._id] = cur
                cur = snippet()
            elif rule.startswith("@"):
                params = rule[1:].split(',')
                cur._type = params[0]
                cur._id = params[1]
                cur._wrapper = self
                cur._params = params[2:]
            elif rule.startswith("{"):
                cur._commands.append(['run', len(cur._blocks)])
                cur._blocks.append(RULE.rule_to_ent_parse(rule))
            elif rule.startswith("/"):
                cur._commands.append(rule[1:].split())

#프로그램 전체에서 사용하는 래퍼
global_wrapper = snippet_wrapper()