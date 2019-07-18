import os.path
import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error
import shlex
import shutil
import subprocess

import yada.config


def get_default_repo(yada_home=yada.config.get_yada_home()):
    return Repo(yada.config.get_default_user_name(),
                yada.config.get_default_repo_name(),
                yada_home=yada_home)


class Module():
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name

    def __str__(self):
        return self.name

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
                      "mkdir -p {dst}".format(dst=destination),
                      interactive=False),
            Operation(lambda: shutil.copy(path, destination),
                      "cp {src} {dst}".format(src=shlex.quote(str(path)),
                                              dst=shlex.quote(str(destination))))
        )

    def install(self):
        for f in self.files_path.glob("**/*"):
            destination = yada.config.get_home() / f.relative_to(self.files_path)
            if f.is_dir():
                yield Operation(lambda: destination.mkdir(parents=True, exist_ok=True),
                                "mkdir -p {}".format(shlex.quote(str(destination))),
                                interactive=True)
            else:
                command = "ln -sf {src} {dst}".format(
                    src=shlex.quote(str(self.repo.path_relative_to(destination.parent) / "modules" / self.name / "files" / f.relative_to(self.files_path))),
                    dst=shlex.quote(str(destination)))
                def backup_and_link():
                    if destination.is_file():
                        shutil.copy(destination,
                                    destination.with_suffix(destination.suffix + '.bkp'))
                    subprocess.call(shlex.split(command), cwd=str(destination.parent))
                yield Operation(backup_and_link,
                                command,
                                interactive=True)

    def push(self, ssh_host):
        for f in self.files_path.glob("**/*"):
            destination = yada.config.get_home() / f.relative_to(self.files_path)
            if f.is_dir():
                command = "ssh {ssh_host} mkdir -p {dir}".format(
                    ssh_host=ssh_host,
                    dir=shlex.quote(str(destination)))
                yield Operation(lambda: subprocess.call(shlex.split(command)),
                                command,
                                interactive=True)
            else:
                command = "scp -q {src} {ssh_host}:{dst}".format(
                    ssh_host=ssh_host,
                    src=shlex.quote(str(f)),
                    dst=shlex.quote(str(destination)))
                def backup_and_link():
                    backup_command = "ssh {ssh_host} {subcommand}".format(
                        ssh_host=ssh_host,
                        subcommand=shlex.quote("sh -c \"cp {dst} {dst}.bkp > /dev/null 2>&1\"".format(
                            dst=destination)))
                    subprocess.call(shlex.split(backup_command))
                    subprocess.call(shlex.split(command))
                yield Operation(backup_and_link,
                                command,
                                interactive=True)


class Repo():
    def __init__(self, user, name, yada_home=yada.config.get_yada_home()):
        self.user = user
        self.name = name
        self.yada_home = pathlib.Path(yada_home)

    def __str__(self):
        return "{user}/{name}".format(user=self.user, name=self.name)

    @property
    def path(self):
        return (self.yada_home / self.user / self.name)

    def create(self):
        self.path.mkdir(parents=True, exist_ok=True)
        subprocess.call(["git", "init"], cwd=str(self.path))

    def exists(self):
        return (self.path / ".git").exists() and (self.path / ".git").is_dir()

    def path_relative_to(self, path):
        common_parent = max(set(list(path.resolve().parents) + [path.resolve()]).intersection(self.path.resolve().parents))
        distance = len(path.parts) - len(common_parent.parts)
        return pathlib.Path(os.path.join(*[".." for _ in range(distance)]) if distance else "") \
            / self.yada_home.relative_to(common_parent) \
            / self.user \
            / self.name

    def module(self, module_name):
        return Module(self, module_name)


class Operation():
    def __init__(self, f, command, interactive=True):
        self.f = f
        self.command = command
        self.interactive = interactive

    def execute(self):
        self.f()
