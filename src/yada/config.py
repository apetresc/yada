import pathlib

from xdg import XDG_DATA_HOME


def get_yada_home():
    return XDG_DATA_HOME / "yada"

def get_home():
    return pathlib.Path.expanduser(pathlib.Path("~"))
