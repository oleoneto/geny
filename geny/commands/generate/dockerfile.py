import click

from geny.core.filesystem.files import File


@click.command()
@click.option("--docker-compose", is_flag=True)
@click.pass_context
def dockerfile(ctx, docker_compose):
    """
    Generate a Dockerfile.
    """

    files = [
        File(name="Dockerfile", template="docker/dockerfile.tpl", context={}),
    ]

    if docker_compose:
        files.append(
            File(
                name="docker-compose.yaml",
                template="docker/docker-compose.tpl",
                context={},
            )
        )

    [
        file.create(
            **ctx.obj,
        )
        for file in files
    ]
