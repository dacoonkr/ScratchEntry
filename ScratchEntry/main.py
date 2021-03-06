import zipfile, tarfile
import json
import os, shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import utils.init as init
import utils.idgen as idgen
import utils.convert.sprites as sprites
import utils.convert.blocks as blocks
import utils.convert.variables as variables
import utils.lib.blocklib as lib

def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, _, files in os.walk(path):
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
        try:
            renderPM.drawToFile(drawing, f"{dir}/image/{i[0:-3]}png", fmt = "PNG")
            renderPM.drawToFile(drawing, f"{dir}/thumb/{i[0:-3]}png", fmt = "PNG")
        except:
            shutil.copyfile(os.path.join("", "empty.png"), 
            os.path.join(f"{dir}/image", f"{i[0:-3]}png"))
    if i[-3::1] == "png":
        inputf.extract(i, f"{dir}/image")
        inputf.extract(i, f"{dir}/thumb")

#입력 스크래치 파일
origin = json.loads(inputd)

#빈 파일 생성
ent = init.initEntfile()

#라이브러리 로드
libs = lib.library()

#전역 변수, 전역 신호 변환하기
vars, varids = variables.convert(origin["targets"][0]["variables"])
lists, listids = variables.convert(origin["targets"][0]["lists"], isList = True)
broadcasts = variables.convert_broadcast(origin["targets"][0]["broadcasts"])
dataids = {**varids, **listids}
for x in vars + lists:
    ent["variables"].append(x)
for x in dataids:
    libs.create_var(x, dataids[x])
for x in broadcasts:
    ent["messages"].append(broadcasts[x])
    libs.create_brd(x, broadcasts[x])

#함수 찾기
for x in origin["targets"]:
    for j in x["blocks"]:
        if x["blocks"][j]["opcode"] == "procedures_prototype":
            libs.create_fn(x["blocks"][j]["mutation"]["proccode"], idgen.getID())

#오브젝트 변환하기
ent["objects"], localvars, localdatas, localbroadcasts, spts_lib, costumes = sprites.convert(origin["targets"])

#지역 변수, 신호, 모양 받기
for x in localvars:
    ent["variables"].append(x)
for x in localbroadcasts:
    ent["messages"].append(broadcasts[x])
    libs.create_brd(x, localbroadcasts[x])
for x in localdatas:
    libs.create_var(x, localdatas[x])
for x in spts_lib:
    libs.create_spt(x, spts_lib[x])
for x in costumes:
    libs.add_costume(x, costumes[x])

#스크립트 전체탐색
rus = []
def script_dfs(script):
    global rus
    if script == None or type(script) == str:
       return
    try:
        for i in script:
            if "content" in i:
                rus.append(i)
                continue
            if type(i) == str: continue
            try: script_dfs(i["statements"][0])
            except: script_dfs(i)
    except:
       pass
    return

#코드 변환하기
for x in range(len(origin["targets"]) - 1): #스테이지 제외한 반복
    script, functions = blocks.convert(origin["targets"][x + 1]["blocks"], libs, x + 1)
    rus = []
    script_dfs(script)
    scripts = json.dumps(script)
    for i in rus:
        d = json.dumps(i)
        scripts = scripts.replace(f"{d},", "")

    ent["objects"][x]["script"] = scripts
    for f in functions:
        ent["functions"].append({"content": json.dumps([f[0]]), "id": libs.get_fn(f[1])})
    for f in rus:
        ent["functions"].append(f)

#변환 결과 쓰기
open('temp/project.json', 'w').write(json.dumps(ent))

#압축하기
tardir('temp', 'output/output.ent')

print("프로젝트 쓰기 완료")