import os
import subprocess
import sys

from ftg.__cli_wrapper.__constants import win32


def open_folder(path_to_folder: str):
    if not os.path.isdir(path_to_folder):
        raise Exception()

    if sys.platform == win32:
        os.startfile(path_to_folder)
    else:
        print(path_to_folder)
        subprocess.call(["xdg-open", path_to_folder])
