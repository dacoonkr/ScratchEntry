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

        for command in self._commands:
            self.run_command(bll, obj, command, in_param, trans)

        for rule in self._blocks:
            out.append(trans.block_build(bll, obj, 0, 0, rule._type, "", rule._params, in_param))

        return out

    def run_command(self, bll: BLL.BLLfile, obj: BLL.BLLobj, command, in_param, trans):
        if command[0] == "sub":
            in_param[command[1]] = self._wrapper._definitions[command[2]].build(bll, obj, [], in_param, trans)

class snippet_wrapper:
    def __init__(self):
        self._definitions = dict() #id:<snippet>
        
        cur = snippet()
        for rule in DICT.snippet_text.split('\n'):
            if rule.startswith("#"): continue
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
                cur._blocks.append(RULE.rule_to_ent_parse(rule))
            elif rule.startswith("/"):
                cur._commands.append(rule[1:].split())

#프로그램 전체에서 사용하는 래퍼
global_wrapper = snippet_wrapper()