import zipfile, tarfile
import json
import os, shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import Sprites, InitEnt
def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))

inputf = zipfile.ZipFile('input\\input.sb3', 'r')
inputd = inputf.read("project.json")
flist = inputf.namelist()

#아웃풋 클리어
folder = 'temp'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)

#리소스 압축해제
for i in flist:
	dir = f"temp/{i[0:2]}/{i[2:4]}";
	if i[-3::1] == "svg":
		inputf.extract(i, f"{dir}/image")
		inputf.extract(i, f"{dir}/thumb")
		drawing = svg2rlg(f"{dir}/image/{i}")
		renderPM.drawToFile(drawing, f"{dir}/image/{i[0:-3]}png", fmt = "PNG")
		renderPM.drawToFile(drawing, f"{dir}/thumb/{i[0:-3]}png", fmt = "PNG")
	if i[-3::1] == "png":
		inputf.extract(i, f"{dir}/image")
		inputf.extract(i, f"{dir}/thumb")

origin = json.loads(inputd)

ent = InitEnt.initEntfile()

ent["objects"] = Sprites.spritesParse(origin["targets"])

open('temp/project.json', 'w').write(json.dumps(ent))

tardir('temp', 'output/output.ent')
print("프로젝트 쓰기 완료")