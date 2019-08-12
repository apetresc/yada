import getpass
import os
import os.path
import sys
if sys.version_info >= (3, 6):
    import pathlib  # pylint: disable=import-error
else:
    import pathlib2 as pathlib  # pylint: disable=import-error
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


class RepoType(click.ParamType):
    name = "Repo"

    def convert(self, value, param, ctx):
        if value is None:
            return None
        elif isinstance(value, yada.repo.Repo):
            return value
        elif "/" in value:
            user, repo = value.split("/")
        else:
            user, repo = yada.config.get_default_user_name(), value
        return yada.repo.Repo(user=user, name=repo, yada_home=ctx.obj["yada-home"])


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
@click.option("--https/--ssh", default=False,
              help="whether to clone via HTTPS or SSH (default)")
@click.option("--repo", "-r", type=RepoType(), default=yada.repo.get_default_repo())
def pull(ctx, https, repo):
    if not repo.exists():
        repo.path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.call(["git", "clone", repo.git_url(protocol="https" if https else "ssh")],
                        cwd=str(repo.path.parent))
    else:
        subprocess.call(["git", "pull"], cwd=str(repo.path))


@cli.command("import")
@click.pass_context
@click.option("--interactive/--no-interactive", "-i", default=False,
              help="query for confirmation before every filesystem operation")
@click.option("--repo", "-r", type=RepoType(), default=yada.repo.get_default_repo())
@click.argument("module", type=str, nargs=1)
@click.argument("files", type=ClickPath(exists=True), nargs=-1)
def import_files(ctx, interactive, repo, module, files):
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
@click.option("--repo", "-r", type=RepoType(), default=yada.repo.get_default_repo())
@click.argument("modules", type=str, nargs=-1)
def install(ctx, interactive, repo, modules):
    for module in modules:
        module = repo.module(module)
        click.secho("Installing module {}...".format(module), fg="green")
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
@click.option("--repo", "-r", type=RepoType(), default=yada.repo.get_default_repo())
@click.argument("module", type=str)
@click.argument("ssh-host", type=str)
def push(ctx, interactive, repo, module, ssh_host):
    module = repo.module(module)

    for operation in module.push(ssh_host):
        click.secho(operation.command, fg="yellow")
        if not ctx.obj["dry-run"] and (not interactive or not operation.interactive or
                                       click.confirm("Take action?")):
            operation.execute()

    click.secho("Done!", fg="green")


@cli.command("info")
@click.pass_context
@click.option("--repo", "-r", type=RepoType(), default=yada.repo.get_default_repo())
@click.argument("module")
def info(ctx, repo, module):
    module = repo.module(module)

    def header(title, width=80):
        ew = (width - len(title) - 2) // 2
        return "=" * ew + " " + title + " " + "=" * (width - (ew + len(title) + 2))

    if not module.exists():
        click.secho("Module {repo}:{module} not found!".format(repo=repo, module=module), fg="red")
        sys.exit(1)
    click.secho("Module {module}".format(module=module), fg="yellow")

    if module.readme_path:
        click.secho(header(module.readme_path.name), fg="yellow")
        click.echo(open(module.readme_path, "r").read())

    if module.files_path.exists():
        click.secho(header("FILES"), fg="yellow")
        for root, _, files in os.walk(str(module.files_path)):
            level = root.replace(str(module.files_path), '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

