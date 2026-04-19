dict_text = """
#작성 시 문법
#스크래치에서 인식 {종류:파람1:파람2>필드1:필드2}
# @     : 파람 중 _menu로 이어지는 것은, 필드값을 바로 불러와 문자열 취급
# @@    : 파람 중 리터럴인 것을 문자열 취급
# &     : 필드 문자열
# *     : 파람 중 STATEMENT
# &&~=~ : 필터링-필드 문자열이 일치하는것만 
#처리 구분(/로 시작)
#var name type label (label이 _new_일시 개별로 생성)
#    cast: 신호
#reg ID obj param1..: 스니펫(청크 타입) 등록
#    obj: name or self
#엔트리에서 출력
#{종류:파람1:파람2} 단, 파람에 {}사용 가능
# &!    : 필드 null값
# &~~   : 필드 문자열값
# &&~~  : number 리터럴 블럭 생성
# @~~   : 리터럴을 생성하지 않고 바로 필드 문자열로 넣음
# ?b    : 스테이지 오브젝트 id
# ?B    : 다음 배경 전환 신호
# *~~   : STATEMENT
# %[a:b,c:d]  : 포맷팅
#    %o: 오브젝트 포인터
#    %k: 키 셀렉터
#    %b: 신호 셀렉터
#    %B: 배경 전환 신호 셀렉터
#    %c: shape 셀렉터
#    %v: 변수 셀렉터
#    %l: 리스트 셀렉터

{event_whenflagclicked}
{when_run_button_click}

{event_whenkeypressed:&KEY_OPTION}
{when_some_key_pressed:&!:@KEY_OPTION%[%k]}

{event_whenbroadcastreceived:&BROADCAST_OPTION}
{when_message_cast:&!:@BROADCAST_OPTION%[%b]}

{event_whenthisspriteclicked}
{when_object_click}

{event_whengreaterthan:VALUE:&&WHENGREATERTHANMENU=TIMER}
/var CAST cast _new_
/reg timer_when self VALUE CAST
{when_message_cast:&!:@CAST}

{event_broadcast:@@BROADCAST_INPUT}
{message_cast:@BROADCAST_INPUT%[%b]}

{event_broadcastandwait:@@BROADCAST_INPUT}
{message_cast_wait:@BROADCAST_INPUT%[%b]}

{event_whenbackdropswitchesto:&BACKDROP}
{when_message_cast:&!:@BACKDROP%[%B]}

{motion_movesteps:STEPS}
{move_direction:STEPS}

{motion_turnright:DEGREES}
{rotate_relative:DEGREES}

{motion_turnleft:DEGREES}
{rotate_relative:{calc_basic:&&0:&MINUS:DEGREES}}

{motion_goto:@TO}
{locate:@TO%[_mouse_:mouse,%o]}

{motion_gotoxy:X:Y}
{locate_xy:X:Y}

{motion_glideto:SECS:@TO}
{locate_object_time:SECS:@TO%[_mouse_:mouse,%o]}

{motion_glidesecstoxy:SECS:X:Y}
{move_xy_time:SECS:X:Y}

{motion_pointindirection:DIRECTION}
{rotate_absolute:DIRECTION}

{motion_pointtowards:@TOWARDS}
{see_angle_object:@TOWARDS%[_mouse_:mouse,%o]}

{motion_changexby:DX}
{move_x:DX}

{motion_setx:X}
{locate_x:X}

{motion_changeyby:DY}
{move_y:DY}

{motion_sety:Y}
{locate_y:Y}

{motion_ifonedgebounce}
{bounce_wall}

{motion_direction}
{coordinate_object:&!:&self:&!:&rotation}

{motion_xposition}
{coordinate_object:&!:&self:&!:&x}

{motion_yposition}
{coordinate_object:&!:&self:&!:&y}

{looks_say:MESSAGE}
{dialog:MESSAGE:&speak}

{looks_think:MESSAGE}
{dialog:MESSAGE:&think}

{looks_sayforsecs:MESSAGE:SECS}
{dialog_time:MESSAGE:SECS:&speak}

{looks_thinkforsecs:MESSAGE:SECS}
{dialog_time:MESSAGE:SECS:&think}

{looks_switchcostumeto:@COSTUME}
{change_to_some_shape:{get_pictures:@COSTUME%[%c]}}

{looks_switchbackdropto:@BACKDROP}
{message_cast:@BACKDROP%[%B]}

{looks_nextcostume}
{change_to_next_shape:&next}

{looks_nextbackdrop}
{message_cast:?B}

{looks_changesizeby:CHANGE}
{change_scale_size:CHANGE}

{looks_setsizeto:SIZE}
{set_scale_size:SIZE}

{looks_changeeffectby:CHANGE:&EFFECT}
{add_effect_amount:@EFFECT%[COLOR:color,BRIGHTNESS:brightness,GHOST:transparency]:CHANGE}

{looks_seteffectto:VALUE:&EFFECT}
{change_effect_amount:@EFFECT%[COLOR:color,BRIGHTNESS:brightness,GHOST:transparency]:VALUE}

{looks_cleargraphiceffects}
{erase_all_effects}

{looks_gotofrontback:&FRONT_BACK}
{change_object_index:@FRONT_BACK%[front:FRONT,back:BACK]}

{looks_goforwardbackwardlayers:NUM:&FORWARD_BACKWARD}
{change_object_index:@FORWARD_BACKWARD%[forward:FORWARD,backward:BACKWARD]}

{looks_show}
{show}

{looks_hide}
{hide}

{looks_size}
{coordinate_object:&!:&self:&!:&size}

{looks_costumenumbername:&NUMBER_NAME}
{coordinate_object:&!:&self:&!:@NUMBER_NAME%[number:picture_index,name:picture_name]}

{looks_backdropnumbername:&NUMBER_NAME}
{coordinate_object:&!:?b:&!:@NUMBER_NAME%[number:picture_index,name:picture_name]}

{control_wait:DURATION}
{wait_second:DURATION}

{control_repeat:TIMES:*SUBSTACK}
{repeat_basic:TIMES:*SUBSTACK}

{control_forever:*SUBSTACK}
{repeat_inf:*SUBSTACK}

{control_if:CONDITION:*SUBSTACK}
{_if:CONDITION:*SUBSTACK}

{control_if_else:CONDITION:*SUBSTACK:*SUBSTACK2}
{if_else:CONDITION:*SUBSTACK:*SUBSTACK2}

{control_wait_until:CONDITION}
{wait_until_true:CONDITION}

{control_repeat_until:CONDITION:*SUBSTACK}
{repeat_while_true:CONDITION:&until:*SUBSTACK}

{control_stop:&STOP_OPTION}
{stop_object:@STOP_OPTION%[this script:thisThread,other scripts in sprite:otherThread]}

{control_start_as_clone}
{when_clone_start}

{control_create_clone_of:@CLONE_OPTION}
{create_clone:@CLONE_OPTION%[_myself_:self,%o]}

{control_delete_this_clone}
{delete_clone}

{sensing_mousedown}
{is_clicked}

{sensing_askandwait:QUESTION}
{ask_and_wait:QUESTION}

{sensing_distanceto:@DISTANCETOMENU}
{distance_something:&!:@DISTANCETOMENU%[_mouse_:mouse,%o]}

{sensing_answer}
{get_canvas_input_value}

{sensing_touchingobject:@TOUCHINGOBJECTMENU}
{reach_something:&!:@TOUCHINGOBJECTMENU%[_mouse_:mouse,_edge_:wall,%o]}

{sensing_keypressed:@KEY_OPTION}
{is_press_some_key:@KEY_OPTION%[%k]}

{sensing_mousex}
{coordinate_mouse:&!:&x}

{sensing_mousey}
{coordinate_mouse:&!:&y}

{sensing_resettimer}
{choose_project_timer_action:&!:&RESET}

{sensing_timer}
{get_project_timer_value}

{sensing_of:@OBJECT:&PROPERTY}
{coordinate_object:&!:@OBJECT%[%o]:&!:@PROPERTY%[x position:x,y position:y,direction:rotation,costume name:picture_name,costume #:picture_index,backdrop name:picture_name,backdrop #:picture_index]}

{sensing_current:&CURRENTMENU}
{get_date:&!:@CURRENTMENU%[DAYOFWEEK:DAY_OF_WEEK]}

{sensing_username}
{get_user_name}

{operator_add:NUM1:NUM2}
{calc_basic:NUM1:&PLUS:NUM2}

{operator_subtract:NUM1:NUM2}
{calc_basic:NUM1:&MINUS:NUM2}

{operator_multiply:NUM1:NUM2}
{calc_basic:NUM1:&MULTI:NUM2}

{operator_divide:NUM1:NUM2}
{calc_basic:NUM1:&DIVIDE:NUM2}

{operator_random:FROM:TO}
{calc_rand:&!:FROM:&!:TO}

{operator_gt:OPERAND1:OPERAND2}
{boolean_basic_operator:OPERAND1:&GREATER:OPERAND2}

{operator_lt:OPERAND1:OPERAND2}
{boolean_basic_operator:OPERAND1:&LESS:OPERAND2}

{operator_equals:OPERAND1:OPERAND2}
{boolean_basic_operator:OPERAND1:&EQUAL:OPERAND2}

{operator_and:OPERAND1:OPERAND2}
{boolean_and_or:OPERAND1:&AND:OPERAND2}

{operator_or:OPERAND1:OPERAND2}
{boolean_and_or:OPERAND1:&OR:OPERAND2}

{operator_not:OPERAND}
{boolean_not:&!:OPERAND}

{operator_join:STRING1:STRING2}
{combine_something:&!:STRING1:&!:STRING2}

{operator_letter_of:STRING:LETTER}
{char_at:&!:STRING:&!:LETTER}

{operator_length:STRING}
{length_of_string:&!:STRING}

{operator_contains:STRING1:STRING2}
{boolean_basic_operator:{index_of_string:&!:STRING1:&!:STRING2}:&GREATER:&&0}

{operator_mod:NUM1:NUM2}
{quotient_and_mod:&!:NUM1:&!:NUM2:&!:&MOD}

{operator_round:NUM}
{calc_operation:&!:NUM:&!:&round}

{operator_mathop:NUM:&OPERATOR}
{calc_operation:&!:NUM:&!:@OPERATOR%[ceiling:ceil,sqrt:root,acos:acos_radian,asin:asin_radian,atan:atan_radian]}
# 10 ^, e ^

{data_setvariableto:VALUE:&VARIABLE}
{set_variable:@VARIABLE%[%v]:VALUE}

{data_changevariableby:VALUE:&VARIABLE}
{change_variable:@VARIABLE%[%v]:VALUE}

{data_showvariable:&VARIABLE}
{show_variable:@VARIABLE%[%v]}

{data_hidevariable:&VARIABLE}
{hide_variable:@VARIABLE%[%v]}

{data_addtolist:ITEM:&LIST}
{add_value_to_list:ITEM:@LIST%[%l]}

{data_deleteoflist:INDEX:&LIST}
{remove_value_from_list:INDEX:@LIST%[%l]}

#{data_deletealloflist}

{data_insertatlist:ITEM:INDEX:&LIST}
{insert_value_to_list:ITEM:@LIST%[%l]:INDEX}

{data_replaceitemoflist:INDEX:ITEM:&LIST}
{change_value_list_index:@LIST%[%l]:INDEX:ITEM}

{data_showlist:&LIST}
{show_list:@LIST%[%l]}

{data_hidelist:&LIST}
{hide_list:@LIST%[%l]}

{data_itemoflist:INDEX:&LIST}
{value_of_index_from_list:&!:@LIST%[%l]:&!:INDEX}

#{data_itemnumoflist:ITEM:&LIST}

{data_lengthoflist:&LIST}
{length_of_list:&!:@LIST%[%l]}

{data_listcontainsitem:ITEM:&LIST}
{is_included_in_list:&!:@LIST%[%l]:&!:ITEM}
"""