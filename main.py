import Filesystem.file as FS
import Scratch.s2b as S2B

import sys, os, shutil

#python main.py mode=a1 input=test/test.rar output=test/out.rar
if __name__ == "__main__":
    arg_mode, arg_in, arg_out = "", "", ""

    #args읽기
    for i in sys.argv:
        if i.startswith("mode="): arg_mode = i[5:]
        if i.startswith("input="): arg_in = i[6:]
        if i.startswith("output="): arg_out = i[7:]
    if arg_mode == "": arg_mode = input("Converting mode: ")
    if arg_in == "": arg_in = input("Input file path: ")
    if arg_out == "": arg_out = input("Output file path: ")
    arg_mode = arg_mode.lower()

    #output 지우기
    folder = ".out"
    os.makedirs(folder, exist_ok = True)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    #변환작업 핸들링
    if arg_mode == "a1":
        file, src_json = FS.import_sb3(arg_in)
        bll, id_map = S2B.s2b(src_json)
        FS.file_move_s2b(id_map, file, folder)
        FS.export_bll(folder, bll.__dict__)
        print("작업이 완료되었습니다.")