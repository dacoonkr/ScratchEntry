import utils.convert.blocks as blocks
import utils.convert.procedures as procedures
import utils.idgen as idgen

import json

def resetlist(list):
    fn_definition = [procedures.get_fn_definition([ idgen.getID() ])]
    
    fnid = idgen.getID()
    fn_call = blocks.getblock(idgen.getID(), f"func_{fnid}", [blocks.getblock(idgen.getID(), "text", ["리스트 비우기"]), None])

    fn_internal_self_call = blocks.getblock(idgen.getID(), f"func_{fnid}",
                                           [blocks.getblock(idgen.getID(), "text", ["리스트 비우기 재귀"]), None])

    fn_internal_delete_item = blocks.getblock(idgen.getID(), f"remove_value_from_list", [1, list, None])
    
    fn_internal_a = blocks.getblock(idgen.getID(), f"text", ['0', None])
    fn_internal_b = blocks.getblock(idgen.getID(), f"length_of_list", [None, list, None])
    
    fn_internal_condition = blocks.getblock(idgen.getID(), "boolean_basic_operator", 
                                            [fn_internal_a, "LESS", fn_internal_b, None])
    
    fn_internal_if = blocks.getblock(idgen.getID(), "_if", [fn_internal_condition, [], None],
                                     statement = [[fn_internal_delete_item, fn_internal_self_call], None])
    
    fn_definition.append(fn_internal_if)

    return {"content": json.dumps([fn_definition]), "id": fnid}, fn_call