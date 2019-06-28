import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error

import yada.config
import yada.repo


home = yada.config.get_home()


def test_repo_relative_to__default():
    repo = yada.repo.get_default_repo()
    
    assert repo.path_relative_to(home / "vim") == pathlib.Path("../.local/share/yada/dot")
    assert repo.path_relative_to(home / "vim/x") == pathlib.Path("../../.local/share/yada/dot")
    assert repo.path_relative_to(home / "vim/") == pathlib.Path("../.local/share/yada/dot")
    assert repo.path_relative_to(home / "a/b/c/d") == pathlib.Path("../../../../.local/share/yada/dot")
    assert repo.path_relative_to(home / "") == pathlib.Path(".local/share/yada/dot")
    assert repo.path_relative_to(home) == pathlib.Path(".local/share/yada/dot")

def test_repo_relative_to__root():
    repo = yada.repo.get_default_repo(yada_home="/etc/yada")

    assert repo.path_relative_to(home / "vim") == pathlib.Path("../../../etc/yada/dot")
