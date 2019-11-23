import json
import os

abspath = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(abspath + "\\dist"):
    abspath = abspath + "\\dist"
path = abspath + "\\main.exe"

try:
    file = open(abspath + "\\settings.json", "rb")
    setting = json.load(file)
    key = setting['key']
except (KeyError, FileNotFoundError, ValueError) as e:
    key = 0

param = "REG ADD \"HKEY_CLASSES_ROOT\\*\\shell\\{2}\\command\" /ve /t REG_SZ /d \"{0}\"%1\" -key {1}\" /f".\
    format(path+" -encrypt ", key, "DANDE로 암호화")
os.system(param)
param = "REG ADD \"HKEY_CLASSES_ROOT\\*\\shell\\{2}\\command\" /ve /t REG_SZ /d \"{0}\"%1\" -key {1}\" /f".\
    format(path+" -decrypt ", key, "DANDE로 복호화")
os.system(param)

os.system("pause")