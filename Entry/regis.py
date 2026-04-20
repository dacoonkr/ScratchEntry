import Entry.regis_dict as DICT
import BLL.bll as BLL
import Entry.snippet as SNIP
import Entry.ent as ENT

class pre_registrator:
    def __init__(self, function_build, trans):
        self._commands = [] # list[list[str]]
        self._function_builder = function_build #todo: 이걸 넘겨받지 않는 형태로 리모델링
        self._translator = trans #todo: 글로벌트랜스레이터 사용
        
        for rule in DICT.registration_text.split('\n'):
            if rule.startswith('/'):
                self._commands.append(rule[1:].split())

    def mount(self, bll: BLL.BLLfile, out: ENT.ENTfile):
        count = 0
        for command in self._commands:
            self.run_command(bll, out, command)
            count += 1
        print(f"로드됨: 프리레지스트레이션 {count}개")

    def run_command(self, bll: BLL.BLLfile, out: ENT.ENTfile, command):
        if command[0] == "freg":
            snip: SNIP.snippet = SNIP.global_wrapper._definitions[command[1]]
            func = BLL.BLLprocedure()
            func._id = bll._id_gen.new_id()
            bll._pre_registrations_map[command[1]] = func._id
            params = []
            for param in snip._params:
                param_id = bll._id_gen.new_id()
                #원본 스크래치에서 인자명이 custom_으로 시작할 경우 오류 일으킬 가능성 있음
                bll._procedure_var_map[f"custom_{param_id}"] = param_id
                func._arguments.append(['s', f"custom_{param_id}"])
                param_block = self._translator.block_build(bll, None, 0, 0, f"stringParam_{param_id}", "", [], dict())
                params.append(param_block)
            codes = snip.build(bll, None, params, dict(), self._translator)
            func_json = self._function_builder(bll, None, [func] + codes, self._translator)
            out._json["functions"].append(func_json)