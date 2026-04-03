import zipfile, tarfile, sys, json
import pickle, os, shutil

#make tar
def make_tar(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, _, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))
#make_tar('temp', 'output/output.ent')

def to_dict(obj):
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    else:
        return {k: to_dict(v) for k, v in obj.__dict__.items()}

def flush_folder(folder):
    os.makedirs(folder, exist_ok = True)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

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
        inputf.getinfo(i).filename = id_map[i[:-4]] + i[-4:] #확장자를 제외하고 id매핑
        inputf.extract(i, f"{output_path}")