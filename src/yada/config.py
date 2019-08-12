import getpass
import pkg_resources
import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from yada.xdg import XDG_DATA_HOME, XDG_CONFIG_HOME


def get_config():
    (XDG_CONFIG_HOME / "yada").mkdir(parents=True, exist_ok=True)
    config_path = XDG_CONFIG_HOME / "yada" / "config.yaml"
    if not config_path.exists():
        with open(str(config_path), "wb") as f:
            f.write(pkg_resources.resource_string("yada.data", "config.yaml"))
    return yaml.load(open(str(config_path), "r").read(), Loader=Loader)

def get_yada_home():
    return XDG_DATA_HOME / "yada"

def get_home():
    return pathlib.Path.home()

def get_default_user_name():
    return get_config().get("username", getpass.getuser())

def get_default_repo_name():
    return get_config().get("default_repo_name", "dot")

