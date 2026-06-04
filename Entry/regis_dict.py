#snippet중 변환 전 필요한 것을 선행으로 추가함 
grammer = """
#작성 시 문법
#처리 구분(/로 시작)
#freg ID: 함수 등록
#    ID: 함수명, system으로 시작할 시 변수와 충돌 가능성 있음
#creg ID: 스니펫(청크 타입) 등록(파람 필요 DEPEND : obj_id or global)
#vreg name: 변수 등록(파람 필요 DEPEND : obj_id or global)
#  obj: name or every
#lreg name: 리스트 등록(무조건 전역)
#vareach name type line src (line:반복문에 포함될 줄 수, 빈 줄 포함X, 반복 중첩X)
#    [~,~,...]
#    %l : 리스트 이름 목록
#    %o : 오브젝트 아이디 목록(Stage제외)
"""

registration_text = """
#지역변수모니터
/lreg **sys_local_monitor
/freg updatevar
#매크로 함수 등록
/freg moveto
/freg seeto
/freg sendcast
/freg waitcast
/freg calcexp
#색관련
/freg clamp_looping
/freg clamp
/freg getbrightness_from_rgb
/freg getsaturation_from_rgb
/freg gethue_from_rgb
/freg setpencolor_by_hsv
#리스트관련
/vareach LIST str 3 %l
/freg clearlist
/freg joinlist
/freg findlist
#오브젝트당
/vareach DEPEND str 5 %o
/vreg isclone 0
/vreg color 0
/vreg saturation 0
/vreg brightness 0
/creg startclone
"""