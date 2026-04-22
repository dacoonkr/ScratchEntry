#snippet중 변환 전 필요한 것을 선행으로 추가함 
grammer = """
#작성 시 문법
#처리 구분(/로 시작)
#freg ID: 함수 등록
#creg ID obj: 스니펫(청크 타입) 등록 
#  obj: name or every
"""

registration_text = """
/freg moveto
/freg seeto
/freg sendcast
/freg waitcast
"""