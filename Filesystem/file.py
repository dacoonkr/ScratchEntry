import zipfile, tarfile, sys, json

#make tar
def make_tar(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, _, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))
#make_tar('temp', 'output/output.ent')

#import sb3
def import_sb3(path):
    inputf = zipfile.ZipFile(path)
    src_json = inputf.read("project.json")
    return inputf, json.loads(src_json)

#파일 옮기기 Scratch -> BLL
def file_move_s2b(id_map, inputf, output_path):
    for i in inputf.namelist():
        if i[-3:] not in ["svg", "png", "wav", "mp3"]:
            continue
        inputf.getinfo(i).filename = output_path + "/" + id_map[i[:-4]] + i[-4:]
        inputf.extract(i, f"{output_path}/src")

#export bll
def export_bll(path, bll):
    open(path + "/code.json", "w").write(json.dumps(bll))