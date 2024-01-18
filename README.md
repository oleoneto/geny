# geny
An extendable file generator

![publish](https://github.com/oleoneto/geny/workflows/publish/badge.svg?branch=master)
![PyPI - Package](https://img.shields.io/pypi/v/geny)
![PyPI - Python](https://img.shields.io/pypi/pyversions/geny)
![PyPI - License](https://img.shields.io/pypi/l/geny)
![PyPI - Downloads](https://img.shields.io/pypi/dm/geny)


- [geny](#geny)
  - [Installation](#installation)
    - [Extending the CLI](#extending-the-cli)
  - [Dependencies](#dependencies)
  - [To Do](#to-do)
  - [Pull requests](#pull-requests)
  - [LICENSE](#license)

## Installation
Install via [pip](https://pypi.org/project/geny):
```bash
pip install geny
```

After installation, the CLI will expose the binary with the name:
```
geny
```

## Extending the CLI

Currently, there are two main ways of extending the functionality of the CLI:
1. Adding your own commands/plugins
2. Overriding the provided resource templates

### Including your own commands

If you would like to extend the functionality of this CLI, you can include your own `plugins/commands` by
setting an environment variable: `GENY_PLUGINS`. Simply set this variable to the path where your plugins are.

Plugin commands are auto-discovered if they are placed under the plugins directory,
but please be sure to do the following for this to work:
1. **Name your package and click command the same**. That is, a package called `get`, for example, should define a `get` command.
2. **Place the command definition within the package's `main.py` module**. For example:
```python
# get/main.py
import click


@click.command()
@click.pass_context
def get(ctx):
    pass
```
3. **Sub-commands should be added to the top-most command group in the package's `main.py` module.**
```python
# get/main.py
import click


@click.group() # <- group
@click.pass_context
def get(ctx):
  pass


@click.command()
@click.pass_context
def foo(ctx):
  pass


get.add_command(foo)
```
4. **Access your commands via your top-most command group.**
```
django-clite get foo
```

**NOTE:** If you would like to skip a plugin/command from being auto-discovered, simply rename the package by either
prepending or appending any number of underscores (`_`). Any code contained within the package will be ignored.

### Overriding the templates

The flag `--templates-dir` can be used to configure an additional path wherein the CLI can look for resource templates.
Alternatively, you can use the environment variable `GENY_TEMPLATES_DIR` for the same purpose.

## Development

### Install from source:
```
git clone https://github.com/oleoneto/geny.git
cd geny
pip install --editable .
```

### Dependencies
Check out [pyproject.toml](pyproject.toml) for all installation dependencies.

## To Do
[Check out our open issues](https://github.com/oleoneto/geny/issues).

## Pull requests
Found a bug? See a typo? Have an idea for new command?
Feel free to submit a pull request with your contributions. They are much welcome and appreciated.

## LICENSE
**geny** is [BSD Licensed](LICENSE).
