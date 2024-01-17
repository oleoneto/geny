# core:decorators
import click


def halt_on_error(f):
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as err:
            click.echo(repr(err), err=True)
            raise click.Abort()

    return wrapper
