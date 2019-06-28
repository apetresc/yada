import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error

from yada.xdg import XDG_DATA_HOME


def get_yada_home():
    return XDG_DATA_HOME / "yada"

def get_home():
    return pathlib.Path.home()

def get_default_repo_name():
    return "dot"
