#python build.py build

from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = ["Crypto.Cipher","encrypt","sys","os"],
                    excludes=["Crypto.Utils"])

exe = [Executable("main.py")]

# 3
setup(
    name='ENCRYPTION',
    version = '0.1',
    author = "이경준",
    description = "아-- 숙제하기싫다",
    options = dict(build_exe = buildOptions),
    executables = exe
)