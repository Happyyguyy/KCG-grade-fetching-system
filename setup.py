from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\Jeong Yeon Cho\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\Jeong Yeon Cho\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6"


options = {
    # sqlite3, tkinter, the font/s, gspread, os, requests, bs4:BeautifulSoup, time, json, textwrap, re
    "includes": ("sqlite3", "gspread", "os", "requests", "time", "json", "textwrap", "re", "time", "startup", "create_card"),
    "include_files": (r".\Fonts", "assembly.config", "db.db", "get_legs.py", "kcggrading_blank.png", "spreadsheets.py", "template.config"),
    "packages": ("bs4"),
    "excludes": ("tkinter")
}
base = "WIN32GUI"

setup(name='Test', version="0.0.1", description="test1",
      executables=[Executable("app.py", base=base)], options={"build_exe": options})
