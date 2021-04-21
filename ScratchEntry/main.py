import zipfile, tarfile
import json
import os, shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import utils.init as init
import utils.convert.sprites as sprites
import utils.convert.variables as variables
import utils.lib.blocklib as lib

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

#입력 스크래치 파일
origin = json.loads(inputd)

#빈 파일 생성
ent = init.initEntfile()

#라이브러리 로드
libs = lib.library()

#오브젝트 변환하기
ent["objects"] = sprites.convert(origin["targets"], libs)

#전역 변수 변환하기
ent["variables"] = variables.convert(origin["targets"][0]["variables"]) \
                 + variables.convert(origin["targets"][0]["lists"], isList = True)

#변환 결과 쓰기
open('temp/project.json', 'w').write(json.dumps(ent))

#압축하기
tardir('temp', 'output/output.ent')

print("프로젝트 쓰기 완료")