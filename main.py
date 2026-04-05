import Filesystem.file as FS
import Scratch.s2b as S2B
import Entry.b2e as B2E
import BLL.bll_logger as LOGGER
import sys, time

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

    print("작업 시작..")
    #인풋
    if arg_in.endswith(".sb3"):
        start_t = time.perf_counter()
        file, src_json = FS.import_sb3(arg_in)
        bll, id_map = S2B.s2b(src_json)
        bll._name = arg_in[:-4]
        FS.file_move_s2b(id_map, file, ".out/bll")
        print(f"변환 완료됨: SB3 → BLL ({int(1000*(time.perf_counter()-start_t))}ms)")
    
    if arg_in.endswith(".ent"):
        pass
        #구현 예정

    #아웃풋
    if arg_out.endswith(".sb3"):
        pass
        #구현 예정
    
    if arg_out.endswith(".ent"):
        start_t = time.perf_counter()
        ent = B2E.b2e(bll, ".out/bll")
        FS.file_move_b2e(".out/bll", ".out/ent")
        FS.make_ent(ent, ".out/ent", arg_out)
        print(f"변환 완료됨: BLL → ENT ({int(1000*(time.perf_counter()-start_t))}ms)")

    if arg_out.endswith(".exe"):
        pass
        #구현 예정

    LOGGER.stats(bll)