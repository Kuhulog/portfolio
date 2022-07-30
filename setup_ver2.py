# coding: utf-8
# cx_Freeze 用セットアップファイル
 
import sys
import os
from cx_Freeze import setup, Executable
import csv

#再起処理の回数を定義
sys.setrecursionlimit(2000)
sys.getrecursionlimit()

Module_Folder_Path = []
Module = []
Icon_Name = []
Exe_Name = []
Des = []
base = []

h = 0
print(os.getcwd())
with open(r"csv\setup.csv", encoding = "utf-8-sig") as f:
    Reader = csv.reader(f)
    for row in Reader:
        if h == 0:
            h += 1
        elif h == 1:
            Module_Folder_Path.append(row[0])
            Module.append(row[1])
            Icon_Name.append(row[2])
            Exe_Name.append(row[3])
            Des.append(row[4])
            base.append(row[5])

if base[0] == "None":
    base = None
else:
    base = "Win32GUI"
   
#対象アイコン
Icon_Folder_Path = Module_Folder_Path[0] + r'\ico'
Icon = Icon_Folder_Path + ("\\") + Icon_Name[0]

os.chdir(Module_Folder_Path[0])

# GUI=有効, CUI=無効 にする
#if sys.platform == 'win32':
    #base = 'Win32GUI'

# exe にしたい python ファイルを指定
#アイコンを設定したい場合は引数にicon='アイコン名.ico'を追加
print(Exe_Name)
if Icon_Name[0] == "":
    exe = Executable(script = Module[0],
                 base = base[0])
else:
    exe = Executable(script = Module[0],
                     base = base,
                     icon = Icon)

# セットアップ
setup(name = Exe_Name[0],
      version = '0.1',
      description = Des[0],
      executables = [exe])