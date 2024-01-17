# commands:destroy
import click

from geny.commands.destroy.dockerfile import dockerfile
from geny.commands.destroy.template import template


@click.group()
@click.pass_context
def destroy(ctx):
    """
    Destroy files.
    """

    ctx.ensure_object(dict)


[
    destroy.add_command(cmd)
    for cmd in [
        dockerfile,
        template,
    ]
]
