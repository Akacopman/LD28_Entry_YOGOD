import sys
from cx_Freeze import setup, Executable

buildOptions = dict(include_files = ['images/', 'sound/']) #folder,relative path. Use tuple like in the single file to set a absolute path.

setup(
    name = "You Only Get One Dollar",
    author = "Ruairidh Carmichael",
    version = "3.1",
    description = "LD28 Entry",
    options = dict(build_exe = buildOptions),
    executables = [Executable("main.py",targetName = ("Game.exe"), base = "Win32GUI", icon = "images/icon.ico", compress = True, appendScriptToExe = True, appendScriptToLibrary = False)]
    )
