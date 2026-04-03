import Filesystem.file as FS
import Scratch.s2b as S2B
import Entry.b2e as B2E

import sys

#python main.py input=test/test.sb3 output=test/out.ent
if __name__ == "__main__":
    arg_in, arg_out = "", ""

    #args읽기
    for i in sys.argv:
        if i.startswith("input="): arg_in = i[6:]
        if i.startswith("output="): arg_out = i[7:]
    if arg_in == "": arg_in = input("Input file path: ")
    if arg_out == "": arg_out = input("Output file path: ")

    #output 지우기
    FS.flush_folder(".out/sb3")
    FS.flush_folder(".out/bll")
    FS.flush_folder(".out/ent")

    bll = None #호환 형식

    #인풋
    if arg_in.endswith(".sb3"):
        file, src_json = FS.import_sb3(arg_in)
        bll, id_map = S2B.s2b(src_json)
        bll._name = arg_in[:-4]
        FS.file_move_s2b(id_map, file, ".out/bll")
        print("BLL로의 변환이 완료되었습니다.")
    
    if arg_in.endswith(".ent"):
        pass
        #구현 예정

    #아웃풋
    if arg_out.endswith(".sb3"):
        pass
        #구현 예정
    
    if arg_out.endswith(".ent"):
        ent = B2E.b2e(bll)
        FS.file_move_b2e(".out/bll", ".out/ent")
        FS.make_ent(ent, ".out/ent", arg_out)
        print("ENT로의 변환이 완료되었습니다.")

    if arg_out.endswith(".exe"):
        pass
        #구현 예정