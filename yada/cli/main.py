import click

@click.group()
@click.option('--dry-run/--no-dry-run', default=False, help='whatever')
@click.pass_context
def cli(ctx, dry_run):
    ctx.ensure_object(dict)
    ctx.obj['dry-run'] = dry_run

@cli.command()
@click.pass_context
def init(ctx):
    click.echo("Hello world: %s" % ctx.obj['dry-run'])

