# commands:generate
import click

from geny.commands.generate.dockerfile import dockerfile
from geny.commands.generate.template import template


@click.group()
@click.pass_context
def generate(ctx):
    """
    Create files.
    """

    ctx.ensure_object(dict)


[
    generate.add_command(cmd)
    for cmd in [
        dockerfile,
        template,
    ]
]
