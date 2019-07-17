import sys
if sys.version_info >= (3, 6):
    from pathlib import Path  # pylint: disable=import-error
else:
    from pathlib2 import Path  # pylint: disable=import-error
import pkg_resources
from pyfakefs import fake_filesystem_unittest

import yada.xdg
import yada.config
import yada.repo


class TestRepo(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs(modules_to_reload=[yada.xdg, yada.config])
        self.fs.add_real_paths([pkg_resources.resource_filename("yada.data", "config.yaml")])
        self.user = yada.config.get_default_user_name()
        self.home = yada.config.get_home()

    def test_repo_relative_to__default(self):
        repo = yada.repo.get_default_repo()
        
        assert repo.path_relative_to(self.home / "vim") == \
            Path("../.local/share/yada/{user}/dot".format(user=self.user))
        assert repo.path_relative_to(self.home / "vim/x") == \
            Path("../../.local/share/yada/{user}/dot".format(user=self.user))
        assert repo.path_relative_to(self.home / "vim/") == \
            Path("../.local/share/yada/{user}/dot".format(user=self.user))
        assert repo.path_relative_to(self.home / "a/b/c/d") == \
            Path("../../../../.local/share/yada/{user}/dot".format(user=self.user))
        assert repo.path_relative_to(self.home / "") == \
            Path(".local/share/yada/{user}/dot".format(user=self.user))
        assert repo.path_relative_to(self.home) == \
            Path(".local/share/yada/{user}/dot".format(user=self.user))

    def test_repo_relative_to__root(self):
        repo = yada.repo.get_default_repo(yada_home="/etc/yada")

        assert repo.path_relative_to(self.home / "vim") == \
            Path("../../../etc/yada/{user}/dot".format(user=self.user))


class TestModule(fake_filesystem_unittest.TestCase):

    def test_module_relative_to(self):
        pass
        #repo = yada.repo.get_default_repo()
        #assert False
