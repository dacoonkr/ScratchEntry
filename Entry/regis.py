import Entry.regis_dict as DICT
import BLL.bll as BLL
import Entry.snippet as SNIP
import Entry.ent as ENT
import BLL.bll_logger as LOGGER

class pre_registrator:
    def __init__(self, function_build, trans):
        self._commands = [] # list[list[str]]
        self._function_builder = function_build #todo: 이걸 넘겨받지 않는 형태로 리모델링
        self._translator = trans #todo: 글로벌트랜스레이터 사용
        
        for rule in DICT.registration_text.split('\n'):
            if len(rule.strip()) == 0: continue
            if rule.startswith('/'):
                self._commands.append(rule[1:].split())

    def mount(self, bll: BLL.BLLfile, out: ENT.ENTfile):
        count = 0
        skip = [False] * len(self._commands)
        for i in range(len(self._commands)):
            if skip[i]: continue
            command = self._commands[i]
            if command[0] == "vareach":
                in_param = dict()
                for j in range(int(command[3])):
                    skip[i + 1 + j] = True
                for item in self.listup(bll, command[4]):
                    if command[2] == "str":
                        in_param[command[1]] = item
                    for j in range(int(command[3])):
                        self.run_command(bll, out, self._commands[i + 1 + j], in_param)
            else: 
                self.run_command(bll, out, command, dict())
            count += 1
        LOGGER.log(1, f"로드됨: 프리레지스트레이션 {count}개")

    def listup(self, bll: BLL.BLLfile, param):
        if param == "%l":
            return [i._id for i in bll._vars if i._type == "list"]

    def run_command(self, bll: BLL.BLLfile, out: ENT.ENTfile, command, in_param):
        if command[0] == "freg":
            snip: SNIP.snippet = SNIP.global_wrapper._definitions[command[1]]
            func = BLL.BLLprocedure()
            func._id = bll._id_gen.new_id()
            params = []
            for param in snip._params:
                param_id = bll._id_gen.new_id()
                #원본 스크래치에서 인자명이 custom_으로 시작할 경우 오류 일으킬 가능성 있음
                bll._procedure_var_map[f"custom_{param_id}"] = param_id
                func._arguments.append(['s', f"custom_{param_id}"])
                param_block = self._translator.block_build(bll, None, 0, 0, f"stringParam_{param_id}", "", [], dict())
                params.append(param_block)
            LOGGER.log(3, f"스니펫 빌드 시작 {command[1]}")
            in_param["SELFCALL"] = f"func_{func._id}"
            name, codes = snip.build(bll, None, params, in_param, self._translator)
            bll._pre_registrations_map[name] = func._id
            func_json = self._function_builder(bll, None, [func] + codes, self._translator)
            out._json["functions"].append(func_json)