try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

from yada.xdg import XDG_DATA_HOME


def get_yada_home():
    return XDG_DATA_HOME / "yada"

def get_home():
    return pathlib.Path.home()

def get_default_repo_name():
    return "dot"
