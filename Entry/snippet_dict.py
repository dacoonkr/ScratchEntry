snippet_text = """
#작성 시 문법
#엔트리에서 출력
#선언 @type,ID, param1..
# stack  (그냥 서브스택 데이터)
# chunk  (하나의 BLLblocks)
# func   (함수 선언자, 커스텀블럭, 파람)
#end    정의 종료
#처리 구분(/로 시작)
#sub name ID: 서브스택
#{종류:파람1:파람2} 단, 파람에 {}사용 가능
# &!   : 필드 null값
# &~~  : 필드 문자열값
# &&~~ : number 리터럴 블럭 생성
# @~~  : 리터럴을 생성하지 않고 바로 필드 문자열로 넣음
# *~~  : STATEMENT
#할당 구문 (선언이 미리 있어야 함)
# @alloc,obj,obj_id,ID, param1..
# @alloc,func,ID, param1..       

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


"""