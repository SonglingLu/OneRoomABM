import cx_Freeze
import sys
import matplotlib

base = None

print(sys.platform)
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("src/gui.py", base=base)]#, icon="config/covid_icon.png")]

includes=["atexit"]
package_list=["tkinter","matplotlib", 'pywinauto']
b_exe = ".//build"
build_options = dict(build_exe=b_exe, packages=package_list, includes=includes)

cx_Freeze.setup(
    name = "GeoACT-Client",
    options = {"build_exe": build_options},#, "include_files":["config/covid_icon.png"]}},
    version = "0.1",
    description = "GeoACT Bus and Class simulations",
    executables = executables
    )
