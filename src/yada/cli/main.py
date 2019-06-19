import os
import os.path
import pathlib
import shlex
import subprocess

import click
import click_pathlib
import delegator
from xdg import XDG_DATA_HOME

import yada.repo


@click.group()
@click.option("--dry-run/--no-dry-run", default=False,
              help="don't actually make any changes to the filesystem")
@click.option("--yada-home",
              type=click_pathlib.Path(file_okay=False, dir_okay=True, writable=True),
              default=str(XDG_DATA_HOME / "yada"),
              help="directory to store yada modules in")
@click.pass_context
def cli(ctx, dry_run, yada_home):
    yada_home.mkdir(parents=True, exist_ok=True)

    ctx.ensure_object(dict)
    ctx.obj["dry-run"] = dry_run
    ctx.obj["yada-home"] = yada_home


@cli.command()
@click.pass_context
@click.option("--name", type=str, default="dot",
              help="")
def init(ctx, name):
    repo = (ctx.obj["yada-home"] / name).resolve()

    if (repo / ".git").exists() and (repo / ".git").is_dir():
        click.secho("Repo {path} already exists.".format(path=repo), fg="yellow")
        return

    repo.mkdir(parents=True, exist_ok=True)
    subprocess.call(["git", "init"], cwd=repo)


@cli.command()
@click.pass_context
@click.argument("location")
def pull(ctx, location):
    subprocess.call(["git", "clone", "git@github.com:{location}".format(location=location)],
                    cwd=ctx.obj["yada-home"])


@cli.command("import")
@click.pass_context
@click.option("--interactive", "-i", default=False,
              help="query for confirmation before every filesystem operation")
@click.argument("module", type=str, nargs=1)
@click.argument("files", type=click_pathlib.Path(exists=True), nargs=-1)
def import_files(ctx, interactive, module, files):
    repo = yada.repo.get_default_repo(ctx.obj["yada-home"])
    module = repo.module(module)
    q = list(files)
    for f in q:
        if f.is_file():
            commands = module.import_file(f)
            for command in commands:
                click.secho(command.command, fg="yellow")
                if not ctx.obj["dry-run"]:
                    command.execute(interactive, ctx.obj["dry-run"])
        elif f.is_dir():
            q += list(f.glob("**/*"))
        else:
            click.secho("{} is an invalid file to import".format(f), fg="red")
