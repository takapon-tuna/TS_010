import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["httplib2", "socks", "encodings"],
    "include_files": [sys.prefix + "/lib/encodings"]
}

setup(
    name="My Python Script",
    version="0.1",
    description="A simple Python script",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)
