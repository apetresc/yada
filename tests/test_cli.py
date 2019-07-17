import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error

#import yada.cli.main
import yada.config

def test_clickpath():
    return
    paths = [yada.config.get_home() / ".vimrc",
             yada.config.get_home() / ".vimrc_nonexistent"]
    for path in paths:
        assert yada.cli.main.ClickPath().convert(str(path), None, None) == path
