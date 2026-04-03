import zipfile, tarfile, sys, json
import pickle, os, shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import Entry.ent as ENT

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

#파일 옮기기 BLL -> Scratch
def file_move_b2e(input_path, output_path):
    for i in os.listdir(input_path):
        if i[-3:] in ["png", "jpg"]:
            os.makedirs(f'{output_path}/temp/{i[0:2]}/{i[2:4]}/image', exist_ok = True)
            shutil.copy(f'{input_path}/{i}', f'{output_path}/temp/{i[0:2]}/{i[2:4]}/image/{i}')
        elif i[-3:] in ["svg"]:
            os.makedirs(f'{output_path}/temp/{i[0:2]}/{i[2:4]}/image', exist_ok = True)
            shutil.copy(f'{input_path}/{i}', f'{output_path}/temp/{i[0:2]}/{i[2:4]}/image/{i}')
            drawing = svg2rlg(f'{input_path}/{i}')
            i = i[:-3] + ".png"
        elif i[-3:] in ["wav", "mp3"]:
            os.makedirs(f'{output_path}/temp/{i[0:2]}/{i[2:4]}/sound', exist_ok = True)
            shutil.copy(f'{input_path}/{i}', f'{output_path}/temp/{i[0:2]}/{i[2:4]}/sound/{i}')

#이미지 get pixel size
def image_getsize(input_path, id):
    if id.endswith(".svg"):
        img = svg2rlg(f'{input_path}/{id}')
        return img.width, img.height
    else: #.png .jpg
        img = Image.open(f'{input_path}/{id}')
    return img.size

#오디오 get duration
def audio_getsize(input_path, id):
    return 1 #일단 되나 테스트해보고, 나중에 수정

def make_ent(ent: ENT.ENTfile, input_path, output_path):
    open(f'{input_path}/temp/project.json', 'w').write(json.dumps(ent._json))
    path = f'{input_path}'
    with tarfile.open(output_path, "w:gz") as tar_handle:
        for root, _, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file), os.path.join(root[len(path):], file))