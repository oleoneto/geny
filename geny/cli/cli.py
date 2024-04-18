import click
import logging
from pathlib import Path
from geny.extensions.combined import AliasedAndDiscoverableGroup
from geny.core.templates.template import TemplateParser


@click.command(
    cls=AliasedAndDiscoverableGroup, context_settings=dict(ignore_unknown_options=True)
)
@click.option("--debug", is_flag=True, help="Enable debug logs.")
@click.option("--dry", is_flag=True, help="Do not modify the file system.")
@click.option("-f", "--force", is_flag=True, envvar="GENY_ENABLE_FORCE", help="Override any conflicting files.")
@click.option("--verbose", is_flag=True, help="Enable verbosity.")
@click.option(
    "--templates-dir",
    "-t",
    envvar="GENY_TEMPLATES_DIR",
    help="Template directory.",
    type=click.Path(),
)
@click.version_option(package_name="geny")
@click.pass_context
def cli(ctx, debug, dry, force, verbose, templates_dir):
    """
    geny

    an extendable file generator.
    """

    # Note for contributors:
    #
    # Commands are auto-discovered if they are placed under the commands directory.
    # But please be sure to do the following for this to work:
    #   1. Name your package and click command the same.
    #   2. Place your command definition within your package's main.py module
    #   3. Any sub-commands of your command should be added to the top-most command in the package's main.py module.
    #
    #   Access your command like so:
    #   `geny my-command my-command-sub-command`
    #
    #   If you would like to skip a plugin/command from being auto-discovered,
    #   simply rename the package by either prepending or appending any number of underscores (_).
    #   Any code contained within the package will be ignored.

    ctx.ensure_object(dict)

    from rich.logging import RichHandler

    FORMAT = "[DRY] %(message)s" if dry else "%(message)s"

    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG if verbose else logging.INFO,
        format=FORMAT,
        handlers=[
            RichHandler(
                log_time_format="",
                show_path=False,
                show_level=False,
                enable_link_path=True,
                markup=True,
            )
        ],
    )

    templates = [Path(__file__).resolve().parent.parent / "template_files"]

    if templates_dir is not None:
        templates.append(Path(templates_dir))

    TemplateParser(
        templates_dir=templates,
        context={},
    )

    ctx.obj["ENABLE_DEBUG"] = debug
    ctx.obj["ENABLE_DRY_RUN"] = dry
    ctx.obj["ENABLE_FORCE"] = force
    ctx.obj["ENABLE_VERBOSITY"] = verbose


if __name__ == "__main__":
    try:
        cli()
    except (KeyboardInterrupt, SystemExit) as e:
        click.echo(f"Exited! {repr(e)}")
