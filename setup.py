import sys, os
from cx_Freeze import setup, Executable

# Temp solution to TCL problem, change directories if needed
os.environ['TCL_LIBRARY'] = "C:\\Python27\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Python27\\tcl\\tk8.5"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "os",
        "jinja2.ext",
        "flask_sqlalchemy",
        "flask_login",
        "flask_wtf",
        "sqlalchemy.dialects.sqlite",
        "sqlalchemy",
        "flask_bcrypt",
        "email"
        ],
    "excludes": ["tkinter", "tcl"],
    "include_files": [
        "config.py",
        "app/templates/",
        "app/static/",
        "LICENSE.txt"
    ]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "FLL Scorepy",
        author='Ryan Foley',
        version = "0.2",
        description = "A FLL event management/ scoring solution ",
        options = {"build_exe": build_exe_options},
        executables = [Executable(
            "run.py",
            base=base,
            copyDependentFiles=True,
            shortcutName="FLL Scorepy",
            shortcutDir="DesktopFolder",)])
