import Filesystem.file as FS
import Scratch.s2b as S2B
import Entry.b2e as B2E
import BLL.bll_logger as LOGGER
import option as OPT
import sys, time, argparse

#python main.py test/test.sb3 test/out.ent
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Scratch → Entry converter")
    parser.add_argument("input", help="Input .sb3 file")
    parser.add_argument("output", nargs="?", help="Output file")
    parser.add_argument('--nocopymark', action='store_true', help='복사본 표시 제거')
    parser.add_argument('--preserve', action='store_true', help='이벤트에 연결되지 않아 실행되지 않는 블럭까지 변환')
    #parser.add_argument('--speedup', action='store_true', help='반복 가속하기')
    OPT.global_option = args = parser.parse_args()

    #output 지우기
    FS.flush_folder(".out/sb3")
    FS.flush_folder(".out/bll")
    FS.flush_folder(".out/ent")

    bll = None #호환 형식

    print("작업 시작..")
    #인풋
    if args.input.endswith(".sb3"):
        start_t = time.perf_counter()
        file, src_json = FS.import_sb3(args.input)
        bll, id_map = S2B.s2b(src_json)
        bll._name = args.input[:-4]
        FS.file_move_s2b(id_map, file, ".out/bll")
        print(f"변환 완료됨: SB3 → BLL ({int(1000*(time.perf_counter()-start_t))}ms)")
    
    #아웃풋
    if args.output.endswith(".ent"):
        start_t = time.perf_counter()
        ent = B2E.b2e(bll, ".out/bll")
        if args.nocopymark:
            print("적용됨: nocopymark")
            ent._json.pop("parent")
            ent._json.pop("origin")
        FS.file_move_b2e(".out/bll", ".out/ent")
        FS.make_ent(ent, ".out/ent", args.output)
        print(f"변환 완료됨: BLL → ENT ({int(1000*(time.perf_counter()-start_t))}ms)")

    LOGGER.stats(bll)