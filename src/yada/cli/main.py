import getpass
import os
import os.path
import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error
import shlex
import subprocess

import click

import yada.config
import yada.repo
from yada.xdg import XDG_DATA_HOME


class ClickPath(click.Path):
    """
    A Click path argument that returns a `Path`, not a string.
    """

    def convert(self, value, param, ctx):
        return pathlib.Path(super(ClickPath, self).convert(value=value, param=param, ctx=ctx))


@click.group()
@click.option("--dry-run/--no-dry-run", default=False,
              help="don't actually make any changes to the filesystem")
@click.option("--yada-home",
              type=ClickPath(file_okay=False, dir_okay=True, writable=True),
              default=str(yada.config.get_yada_home()),
              help="directory to store yada modules in")
@click.pass_context
def cli(ctx, dry_run, yada_home):
    yada_home.mkdir(parents=True, exist_ok=True)

    ctx.ensure_object(dict)
    ctx.obj["dry-run"] = dry_run
    ctx.obj["yada-home"] = yada_home


@cli.command()
@click.pass_context
@click.option("--name", type=str, default=yada.config.get_default_repo_name(),
              help="")
def init(ctx, name):
    repo = yada.repo.Repo(user=yada.config.get_default_user_name(), name=name)

    if repo.exists():
        click.secho("Repo {path} already exists.".format(path=repo), fg="yellow")
    else:
        repo.create()


@cli.command()
@click.pass_context
@click.argument("location", type=str, required=False, default="{user}/{repo}".format(
    user=getpass.getuser(), repo=yada.config.get_default_repo_name()))
def pull(ctx, location):
    user, _ = location.split("/")
    (ctx.obj["yada-home"] / user).mkdir(parents=True, exist_ok=True)
    subprocess.call(["git", "clone", "git@github.com:{location}".format(location=location)],
                    cwd=ctx.obj["yada-home"] / user)


@cli.command("import")
@click.pass_context
@click.option("--interactive/--no-interactive", "-i", default=False,
              help="query for confirmation before every filesystem operation")
@click.argument("module", type=str, nargs=1)
@click.argument("files", type=ClickPath(exists=True), nargs=-1)
def import_files(ctx, interactive, module, files):
    repo = yada.repo.get_default_repo(ctx.obj["yada-home"])
    module = repo.module(module)
    q = list(files)
    for f in q:
        if f.is_file():
            operations = module.import_file(f)
            for operation in operations:
                click.secho(operation.command, fg="yellow")
                if not ctx.obj["dry-run"] and (not interactive or not operation.interactive or
                                               click.confirm("Take action?")):
                    operation.execute()
        elif f.is_dir():
            q += list(f.glob("**/*"))
        else:
            click.secho("{} is an invalid file to import".format(f), fg="red")


@cli.command("install")
@click.pass_context
@click.option("--interactive/--no-interactive", "-i", default=False,
              help="query for confirmation before every filesystem operation")
@click.argument("module", type=str)
def install(ctx, interactive, module):
    repo = yada.repo.get_default_repo(ctx.obj["yada-home"])
    module = repo.module(module)

    for operation in module.install():
        click.secho(operation.command, fg="yellow")
        if not ctx.obj["dry-run"] and (not interactive or not operation.interactive or
                                       click.confirm("Take action?")):
            operation.execute()

    click.secho("Done!", fg="green")


@cli.command("push")
@click.pass_context
@click.option("--interactive/--no-interactive", "-i", default=False,
              help="query for confirmation before each file upload")
@click.argument("module", type=str)
@click.argument("ssh-host", type=str)
def push(ctx, interactive, module, ssh_host):
    repo = yada.repo.get_default_repo(ctx.obj["yada-home"])
    module = repo.module(module)

    for operation in module.push(ssh_host):
        click.secho(operation.command, fg="yellow")
        if not ctx.obj["dry-run"] and (not interactive or not operation.interactive or
                                       click.confirm("Take action?")):
            operation.execute()

    click.secho("Done!", fg="green")


