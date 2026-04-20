grammer = """
#작성 시 문법
#엔트리에서 출력
#선언 @type,ID, param1..
# stack  (그냥 서브스택 데이터)
# chunk  (하나의 BLLblocks)
# func   (함수 선언자, 커스텀블럭, 파람)
#end    정의 종료
#처리 구분(/로 시작)
#sub name ID: 서브스택
#(내부적으로 사용) run idx: ent_rule에 따라 블럭 생성
#var name type label (label이 _new_일시 개별로 생성)
#    lit: 리터럴 블럭
#    str: 필드 문자열값
#vareach name type line src (line:반복문에 포함될 줄 수, 빈 줄 포함X, 반복 중첩X)
#    [~,~,...]
#    %o : 오브젝트 이름 목록
#{종류:파람1:파람2} 단, 파람에 {}사용 가능
# &!   : 필드 null값
# &~~  : 필드 문자열값
# &&~~ : number 리터럴 블럭 생성
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
{locate_object_time:SECS:@NAME%[_mouse_:mouse]}
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

"""