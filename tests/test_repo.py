import pathlib

import yada.repo


def test_relative_to__default():
    repo = yada.repo.get_default_repo()
    
    assert repo.path_relative_to("/home/apetresc/vim") == pathlib.Path("../.local/share/yada/dot")
    assert repo.path_relative_to("/home/apetresc/a/b/c/d") == pathlib.Path("../../../../.local/share/yada/dot")

def test_relative_to__root():
    repo = yada.repo.get_default_repo(yada_home="/etc/yada")

    assert repo.path_relative_to("/home/apetresc/vim") == pathlib.Path("../../etc/yada/dot")
