import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Program Files\Python37\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files\Python37\tcl\tk8.6"

executables = [cx_Freeze.Executable("main.py", base=base, icon="icon.ico")]


cx_Freeze.setup(
    name = "Inventry Managment System",
    options = {"build_exe": {"packages":["tkinter","os","PyQt5"], "include_files":["icon.ico",'DB','Billing_Saved_Data','QR_Code','src','ToolBar','xlwt','tcl86t.dll','tk86t.dll','sqlite3.dll','Login2.ui','user.ui','res_rc.py','res.qrc','toolmenu.py']}},
    version = "8.3",
    description = "Shivanya Clothing Center | Developed By SHUBHAM LOHAR",
    executables = executables
    )
