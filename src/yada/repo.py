import os.path
import pathlib
import shlex
import shutil

import yada.config


def get_default_repo(yada_home=yada.config.get_yada_home()):
    return Repo("dot", yada_home=yada_home)


class Module():
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name

    @property
    def path(self):
        return self.repo.path / "modules" / self.name

    @property
    def files_path(self):
        return self.path / "files"

    def create(self):
        self.files_path.mkdir(parents=True, exist_ok=True)

    def import_file(self, path):
        if not path.is_absolute():
            path = pathlib.Path.cwd() / path
        destination = self.files_path / path.relative_to(yada.config.get_home())

        return (
            Operation(lambda: destination.parent.mkdir(parents=True, exist_ok=True),
                      "mkdir -p {dst}".format(dst=destination)),
            Operation(lambda: shutil.copy(path, destination),
                      "cp {src} {dst}".format(src=shlex.quote(str(path)),
                                              dst=shlex.quote(str(destination))))
        )


class Repo():
    def __init__(self, name, yada_home=yada.config.get_yada_home()):
        self.name = name
        self.yada_home = pathlib.Path(yada_home)

    @property
    def path(self):
        return (self.yada_home / self.name)

    def path_relative_to(self, path):
        common_parent = os.path.commonpath([path, self.path])
        return pathlib.Path(
            os.path.join(*[".." for _ in range(
                len(str(path).split(os.path.sep)) - len(common_parent.split(os.path.sep)))])) \
            / self.yada_home.relative_to(common_parent) \
            / self.name

    def module(self, module_name):
        return Module(self, module_name)


class Operation():
    def __init__(self, f, command):
        self.f = f
        self.command = command

    def execute(self, interactive, dry_run):
        self.f()
