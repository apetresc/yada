import sys
if sys.version_info >= (3, 6):
    from pathlib import Path  # pylint: disable=import-error
else:
    from pathlib2 import Path  # pylint: disable=import-error

import yada.config
import yada.repo


user = yada.config.get_default_user_name()
home = yada.config.get_home()


def test_repo_relative_to__default():
    repo = yada.repo.get_default_repo()
    
    assert repo.path_relative_to(home / "vim") == Path("../.local/share/yada/{user}/dot".format(user=user))
    assert repo.path_relative_to(home / "vim/x") == Path("../../.local/share/yada/{user}/dot".format(user=user))
    assert repo.path_relative_to(home / "vim/") == Path("../.local/share/yada/{user}/dot".format(user=user))
    assert repo.path_relative_to(home / "a/b/c/d") == Path("../../../../.local/share/yada/{user}/dot".format(user=user))
    assert repo.path_relative_to(home / "") == Path(".local/share/yada/{user}/dot".format(user=user))
    assert repo.path_relative_to(home) == Path(".local/share/yada/{user}/dot".format(user=user))

def test_repo_relative_to__root():
    repo = yada.repo.get_default_repo(yada_home="/etc/yada")

    assert repo.path_relative_to(home / "vim") == Path("../../../etc/yada/{user}/dot".format(user=user))


def test_module_relative_to():
    repo = yada.repo.get_default_repo()

    #assert False
