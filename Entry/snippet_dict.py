grammer = """
#작성 시 문법
#엔트리에서 출력
#선언 @type,ID,param1..
# stack  (그냥 서브스택 데이터)
# chunk  (하나의 BLLblocks)
# func   (함수 선언자, 커스텀블럭, 파람)
#end    정의 종료
#처리 구문(/로 시작)
#sub name ID: 서브스택
#append name: 청크를 그냥 이어붙임
#(내부적으로 사용) run idx: ent_rule에 따라 블럭 생성
#var name type label (label이 _new_일시 개별로 생성)
#    lit: 리터럴 블럭
#    str: 필드 문자열값
#    blk: 엔트리 블럭(Entrule{} 사용)
#name str1 str2 str3... : 각 인자를 모두 합친 이름으로 함수 이름 변경
#    &NAME: NAME변수(str타입) 사용
#local name: 함수 내부 로컬 변수 선언
#vareach name type line src (line:반복문에 포함될 줄 수, 빈 줄 포함X, 반복 중첩X)
#    [~,~,...]
#    %o : 오브젝트 이름 목록
#    %b : 신호 이름 목록
#{종류:파람1:파람2} 단, 파람에 {}사용 가능
# !~~   : 프리레지스트레이션 함수 호출
# !&~~  : 프리레지스트레이션 함수 호출(변수값의 함수 이름 호출)
# &!   : 필드 null값
# &~~  : 필드 문자열값
# &&~~ : number 리터럴 블럭 생성
# &@~~ : number 리터럴 블럭 생성(파라미터 사용)
# +    : 필드 문자열 값을 사용하되, 리터럴을 생성해 변환하여 사용
# @~~  : 리터럴을 생성하지 않고 바로 필드 문자열로 넣음
# *~~  : STATEMENT
"""

snippet_text = """

@stack,timer_when_substack
{wait_until_true:{boolean_basic_operator:{get_project_timer_value}:&GREATER:TIME}}
{message_cast:@CAST}
{wait_until_true:{boolean_basic_operator:{get_project_timer_value}:&LESS:TIME}}
end

@chunk,timer_when,TIME,CAST
/sub SUBSTK timer_when_substack
{when_run_button_click}
{repeat_inf:*SUBSTK}
end

@stack,moveto_substack_random
{move_xy_time:SECS:{calc_rand:&!:&&-240:&!:&&240}:{calc_rand:&!:&&-180:&!:&&180}}
end

@stack,moveto_substack
{locate_object_time:SECS:@NAME%[_mouse_:mouse,%o]}
end

@func,moveto,TARGET,SECS
/var NAME str _random_
/sub SUBSTK moveto_substack_random
{_if:{boolean_basic_operator:TARGET:&EQUAL:+NAME}:*SUBSTK}

/var NAME str _mouse_
/sub SUBSTK moveto_substack
{_if:{boolean_basic_operator:TARGET:&EQUAL:+NAME}:*SUBSTK}

/vareach NAME str 2 %o
/sub SUBSTK moveto_substack
{_if:{boolean_basic_operator:TARGET:&EQUAL:+NAME}:*SUBSTK}
end

@stack,seeto_substack
{see_angle_object:@NAME%[_mouse_:mouse,%o]}
end

@func,seeto,TARGET
/var NAME str _mouse_
/sub SUBSTK seeto_substack
{_if:{boolean_basic_operator:TARGET:&EQUAL:+NAME}:*SUBSTK}

/vareach NAME str 2 %o
/sub SUBSTK seeto_substack
{_if:{boolean_basic_operator:TARGET:&EQUAL:+NAME}:*SUBSTK}
end

@func,sendcast_substack
{message_cast:@NAME%[%b]}
end

@func,sendcast,CAST
/vareach NAME str 2 %b
/sub SUBSTK sendcast_substack
{_if:{boolean_basic_operator:CAST:&EQUAL:+NAME}:*SUBSTK}
end

@func,waitcast_substack
{message_cast_wait:@NAME%[%b]}
end

@func,waitcast,CAST
/vareach NAME str 2 %b
/sub SUBSTK waitcast_substack
{_if:{boolean_basic_operator:CAST:&EQUAL:+NAME}:*SUBSTK}
end

@stack,clearlist_substack
{!&SELFCALL}
end

@func,clearlist
/name clear &LIST
{remove_value_from_list:{length_of_list:&!:@LIST}:@LIST}
/sub SUBSTK clearlist_substack
{_if:{boolean_basic_operator:{length_of_list:&!:@LIST}:&GREATER:&&0}:*SUBSTK}
end

@chunk,repskip
{wait_until_true:{boolean_not:&!:{continue_repeat}}}
end

@stack,calcexp_substack
{set_func_variable:@SUM:{calc_basic:{get_func_variable:@SUM}:&PLUS:{get_func_variable:@TERM}}}
{set_func_variable:@I:{calc_basic:{get_func_variable:@I}:&PLUS:&&1}}
{set_func_variable:@TERM:{calc_basic:{get_func_variable:@TERM}:&MULTI:@EXP}}
{set_func_variable:@TERM:{calc_basic:{get_func_variable:@TERM}:&DIVIDE:{get_func_variable:@I}}}
/append repskip
end

@stack,calcexp_return
{get_func_variable:@SUM}
end

@func,calcexp,EXP
/local SUM
/local TERM
/local I
{set_func_variable:@SUM:&&0}
{set_func_variable:@TERM:&&1}
{set_func_variable:@I:&&0}
/sub SUBSTK calcexp_substack
{repeat_basic:&&100:*SUBSTK}
/sub RET calcexp_return
/var FUNC_RETURN blk RET
end

@stack,joinlist_substack
{set_func_variable:@IDX:{calc_basic:{get_func_variable:@IDX}:&PLUS:&&1}}
{set_func_variable:@RET:{combine_something:&!:{get_func_variable:@RET}:&!:&& }}
{set_func_variable:@RET:{combine_something:&!:{get_func_variable:@RET}:&!:{value_of_index_from_list:&!:@LIST:&!:{get_func_variable:@IDX}}}}
/append repskip
end

@stack,joinlist_ifstack
{set_func_variable:@IDX:&&1}
{set_func_variable:@RET:{value_of_index_from_list:&!:@LIST:&!:&&1}}
/sub SUBSTK joinlist_substack
{repeat_basic:{calc_basic:{length_of_list:&!:@LIST}:&MINUS:&&1}:*SUBSTK}
end

@stack,joinlist_return
{replace_string:&!:{get_func_variable:@RET}:&!:&&$marker_empty$:&!:&&}
end

@func,joinlist
/name join &LIST
/local RET
/local IDX
# 버그 (빈 문자열이 0으로 대체됨) 때문에 빈 문자열을 $marker_empty$로 표시
{set_func_variable:@RET:&&$marker_empty$}
/sub IFSTK joinlist_ifstack
{_if:{boolean_basic_operator:&&0:&LESS:{length_of_list:&!:@LIST}}:*IFSTK}
/sub RET joinlist_return
/var FUNC_RETURN blk RET
end

@stack,findlist_ifstack
{set_func_variable:@RET:{get_func_variable:@IDX}}
{stop_repeat}
end

@stack,findlist_substack
/sub IFSTK findlist_ifstack
{_if:{boolean_basic_operator:ITEM:&EQUAL:{value_of_index_from_list:&!:@LIST:&!:{get_func_variable:@IDX}}}:*IFSTK}
{set_func_variable:@IDX:{calc_basic:{get_func_variable:@IDX}:&PLUS:&&1}}
/append repskip
end

@stack,ret_return
{get_func_variable:@RET}
end

@func,findlist,ITEM
/name find &LIST
/local RET
/local IDX
{set_func_variable:@RET:&&0}
{set_func_variable:@IDX:&&1}
/sub SUBSTK findlist_substack
{repeat_basic:{length_of_list:&!:@LIST}:*SUBSTK}
/sub RET ret_return
/var FUNC_RETURN blk RET
end

@chunk,startclone
{when_clone_start}
/var VAR str isclone
{set_variable:@VAR%[%plv]:&&1}
end

@chunk,updatevar_substack
{change_value_list_index:&**sys_local_monitor%[%l]:IDX:VALUE}
end

@func,updatevar,CLONE,IDX,VALUE
/sub SUBSTK updatevar_substack
{_if:{boolean_basic_operator:CLONE:&EQUAL:&&0}:*SUBSTK}
end

@chunk,updatevarcall,CLONE,IDX,VAR
{!updatevar:{get_variable:@CLONE}:&@IDX:{get_variable:@VAR}}
end

@chunk,clamp_looping_minus
{set_func_variable:@RET:{calc_basic:{get_func_variable:@RET}:&MINUS:LIMIT}}
/append repskip
end

@chunk,clamp_looping_plus
{set_func_variable:@RET:{calc_basic:{get_func_variable:@RET}:&PLUS:LIMIT}}
/append repskip
end

@func,clamp_looping,DATA,LIMIT
/local RET
{set_func_variable:@RET:DATA}
/sub MINUS clamp_looping_minus
/sub PLUS clamp_looping_plus
{repeat_while_true:{boolean_basic_operator:{get_func_variable:@RET}:&LESS:LIMIT}:&until:*MINUS}
{repeat_while_true:{boolean_basic_operator:{get_func_variable:@RET}:&GREATER_OR_EQUAL:&&0}:&until:*PLUS}
/sub RET ret_return
/var FUNC_RETURN blk RET
end

@chunk,clamp_max
{set_func_variable:@RET:LIMIT}
end

@chunk,clamp_min
{set_func_variable:@RET:&&0}
end

@func,clamp,DATA,LIMIT
/local RET
{set_func_variable:@RET:DATA}
/sub MAX clamp_max
/sub MIN clamp_min
{_if:{boolean_basic_operator:{get_func_variable:@RET}:&GREATER_OR_EQUAL:LIMIT}:*MAX}
{_if:{boolean_basic_operator:{get_func_variable:@RET}:&LESS:&&0}:*MIN}
/sub RET ret_return
/var FUNC_RETURN blk RET
end

@stack,min_three_rgb_substack_min_g
{set_func_variable:@VMIN:{get_func_variable:@g}}
end

@stack,min_three_rgb_substack_min_b
{set_func_variable:@VMIN:{get_func_variable:@b}}
end

@stack,max_three_rgb_substack_max_g
{set_func_variable:@VMAX:{get_func_variable:@g}}
end

@stack,max_three_rgb_substack_max_b
{set_func_variable:@VMAX:{get_func_variable:@b}}
end

@stack,minmax_three_rgb
{set_func_variable:@VMIN:{get_func_variable:@r}}
{set_func_variable:@VMAX:{get_func_variable:@r}}
/sub MIN_G min_three_rgb_substack_min_g
/sub MIN_B min_three_rgb_substack_min_b
{_if:{boolean_basic_operator:{get_func_variable:@VMIN}:&GREATER:{get_func_variable:@g}}:*MIN_G}
{_if:{boolean_basic_operator:{get_func_variable:@VMIN}:&GREATER:{get_func_variable:@b}}:*MIN_B}
/sub MAX_G max_three_rgb_substack_max_g
/sub MAX_B max_three_rgb_substack_max_b
{_if:{boolean_basic_operator:{get_func_variable:@VMAX}:&LESS:{get_func_variable:@g}}:*MAX_G}
{_if:{boolean_basic_operator:{get_func_variable:@VMAX}:&LESS:{get_func_variable:@b}}:*MAX_B}
end

@func,getbrightness_from_rgb,R,G,B
/local VMAX
/local VMIN
/local r
/local g
/local b
/local RET
{set_func_variable:@r:{calc_basic:R:&DIVIDE:&&255}}
{set_func_variable:@g:{calc_basic:G:&DIVIDE:&&255}}
{set_func_variable:@b:{calc_basic:B:&DIVIDE:&&255}}
/append minmax_three_rgb

{set_func_variable:@RET:{calc_basic:{get_func_variable:@VMAX}:&MULTI:&&100}}
/sub RET ret_return
/var FUNC_RETURN blk RET
end

@stack,getsaturation_from_rgb_substack
{set_func_variable:@RET:{calc_basic:{calc_basic:{calc_basic:{get_func_variable:@VMAX}:&MINUS:{get_func_variable:@VMIN}}:&DIVIDE:{get_func_variable:@VMAX}}:&MULTI:&&100}}
end

@func,getsaturation_from_rgb,R,G,B
/local VMAX
/local VMIN
/local r
/local g
/local b
/local RET
{set_func_variable:@r:{calc_basic:R:&DIVIDE:&&255}}
{set_func_variable:@g:{calc_basic:G:&DIVIDE:&&255}}
{set_func_variable:@b:{calc_basic:B:&DIVIDE:&&255}}
/append minmax_three_rgb

{set_func_variable:@RET:&&0}
/sub IFSTK getsaturation_from_rgb_substack
{_if:{boolean_basic_operator:{get_func_variable:@VMAX}:&NOT_EQUAL:&&0}:*IFSTK}

/sub RET ret_return
/var FUNC_RETURN blk RET
end

@stack,gethue_from_rgb_r
{set_func_variable:@RET:{calc_basic:{calc_basic:{get_func_variable:@g}:&MINUS:{get_func_variable:@b}}:&DIVIDE:{get_func_variable:@C}}}
end

@stack,gethue_from_rgb_g
{set_func_variable:@RET:{calc_basic:{calc_basic:{get_func_variable:@b}:&MINUS:{get_func_variable:@r}}:&DIVIDE:{get_func_variable:@C}}}
{set_func_variable:@RET:{calc_basic:{get_func_variable:@RET}:&PLUS:&&2}}
end

@stack,gethue_from_rgb_b
{set_func_variable:@RET:{calc_basic:{calc_basic:{get_func_variable:@r}:&MINUS:{get_func_variable:@g}}:&DIVIDE:{get_func_variable:@C}}}
{set_func_variable:@RET:{calc_basic:{get_func_variable:@RET}:&PLUS:&&4}}
end

@stack,gethue_from_rgb_substack
/sub SUB_R gethue_from_rgb_r
/sub SUB_G gethue_from_rgb_g
/sub SUB_B gethue_from_rgb_b
{_if:{boolean_basic_operator:{get_func_variable:@VMAX}:&EQUAL:{get_func_variable:@r}}:*SUB_R}
{_if:{boolean_basic_operator:{get_func_variable:@VMAX}:&EQUAL:{get_func_variable:@g}}:*SUB_G}
{_if:{boolean_basic_operator:{get_func_variable:@VMAX}:&EQUAL:{get_func_variable:@b}}:*SUB_B}
{set_func_variable:@RET:{!clamp_looping:{calc_basic:{get_func_variable:@RET}:&MULTI:&&16.666666}:&&100}}
end

@func,gethue_from_rgb,R,G,B
/local VMAX
/local VMIN
/local r
/local g
/local b
/local RET
/local C
{set_func_variable:@r:{calc_basic:R:&DIVIDE:&&255}}
{set_func_variable:@g:{calc_basic:G:&DIVIDE:&&255}}
{set_func_variable:@b:{calc_basic:B:&DIVIDE:&&255}}
/append minmax_three_rgb

{set_func_variable:@C:{calc_basic:{get_func_variable:@VMAX}:&MINUS:{get_func_variable:@VMIN}}}
{set_func_variable:@RET:&&0}
/sub IFSTK gethue_from_rgb_substack
{_if:{boolean_basic_operator:{get_func_variable:@C}:&GREATER:&&0}:*IFSTK}

/sub RET ret_return
/var FUNC_RETURN blk RET
end

@chunk,updatecolor
/var VAR str color
{set_variable:@VAR%[%plv]:{!gethue_from_rgb:{change_hex_to_rgb:COLOR:&r}:{change_hex_to_rgb:COLOR:&g}:{change_hex_to_rgb:COLOR:&b}}}
/var VAR str brightness
{set_variable:@VAR%[%plv]:{!getbrightness_from_rgb:{change_hex_to_rgb:COLOR:&r}:{change_hex_to_rgb:COLOR:&g}:{change_hex_to_rgb:COLOR:&b}}}
/var VAR str saturation
{set_variable:@VAR%[%plv]:{!getsaturation_from_rgb:{change_hex_to_rgb:COLOR:&r}:{change_hex_to_rgb:COLOR:&g}:{change_hex_to_rgb:COLOR:&b}}}
end

@stack,setpencolor_by_hsv_substack1
{set_func_variable:@r:{get_func_variable:@C}}
{set_func_variable:@g:{get_func_variable:@X}}
{set_func_variable:@b:&&0}
end

@stack,setpencolor_by_hsv_substack2
{set_func_variable:@r:{get_func_variable:@X}}
{set_func_variable:@g:{get_func_variable:@C}}
{set_func_variable:@b:&&0}
end

@stack,setpencolor_by_hsv_substack3
{set_func_variable:@r:&&0}
{set_func_variable:@g:{get_func_variable:@C}}
{set_func_variable:@b:{get_func_variable:@X}}
end

@stack,setpencolor_by_hsv_substack4
{set_func_variable:@r:&&0}
{set_func_variable:@g:{get_func_variable:@X}}
{set_func_variable:@b:{get_func_variable:@C}}
end

@stack,setpencolor_by_hsv_substack5
{set_func_variable:@r:{get_func_variable:@X}}
{set_func_variable:@g:&&0}
{set_func_variable:@b:{get_func_variable:@C}}
end

@stack,setpencolor_by_hsv_substack6
{set_func_variable:@r:{get_func_variable:@C}}
{set_func_variable:@g:&&0}
{set_func_variable:@b:{get_func_variable:@X}}
end

@func,setpencolor_by_hsv,H,S,V
/local C
/local h
/local X
/local m
/local tmp
{set_func_variable:@C:{calc_basic:{calc_basic:S:&MULTI:V}:&DIVIDE:&&10000}}
{set_func_variable:@h:{calc_basic:H:&DIVIDE:&&16.666666}}
{set_func_variable:@tmp:{quotient_and_mod:&!:{get_func_variable:@h}:&!:&&2:&!:&MOD}}
{set_func_variable:@tmp:{calc_operation:&!:{calc_basic:{get_func_variable:@tmp}:&MINUS:&&1}:&!:&abs}}
{set_func_variable:@X:{calc_basic:{get_func_variable:@C}:&MULTI:{calc_basic:&&1:&MINUS:{get_func_variable:@tmp}}}}
{set_func_variable:@m:{calc_basic:{calc_basic:V:&DIVIDE:&&100}:&MINUS:{get_func_variable:@C}}}
/local r
/local g
/local b
/sub IFSTK setpencolor_by_hsv_substack6
{_if:{boolean_basic_operator:{get_func_variable:@h}:&LESS:&&6.1}:*IFSTK}
/sub IFSTK setpencolor_by_hsv_substack5
{_if:{boolean_basic_operator:{get_func_variable:@h}:&LESS:&&5}:*IFSTK}
/sub IFSTK setpencolor_by_hsv_substack4
{_if:{boolean_basic_operator:{get_func_variable:@h}:&LESS:&&4}:*IFSTK}
/sub IFSTK setpencolor_by_hsv_substack3
{_if:{boolean_basic_operator:{get_func_variable:@h}:&LESS:&&3}:*IFSTK}
/sub IFSTK setpencolor_by_hsv_substack2
{_if:{boolean_basic_operator:{get_func_variable:@h}:&LESS:&&2}:*IFSTK}
/sub IFSTK setpencolor_by_hsv_substack1
{_if:{boolean_basic_operator:{get_func_variable:@h}:&LESS:&&1}:*IFSTK}
{set_func_variable:@r:{calc_basic:{calc_basic:{get_func_variable:@r}:&PLUS:{get_func_variable:@m}}:&MULTI:&&255}}
{set_func_variable:@g:{calc_basic:{calc_basic:{get_func_variable:@g}:&PLUS:{get_func_variable:@m}}:&MULTI:&&255}}
{set_func_variable:@b:{calc_basic:{calc_basic:{get_func_variable:@b}:&PLUS:{get_func_variable:@m}}:&MULTI:&&255}}
{set_color:{change_rgb_to_hex:{get_func_variable:@r}:{get_func_variable:@g}:{calc_operation:&!:{get_func_variable:@b}:&!:&round}}}
end

@chunk,applyhsv
/var VAR1 str color
/var VAR2 str saturation
/var VAR3 str brightness
{!setpencolor_by_hsv:{get_variable:@VAR1%[%plv]}:{get_variable:@VAR2%[%plv]}:{get_variable:@VAR3%[%plv]}}
end
"""