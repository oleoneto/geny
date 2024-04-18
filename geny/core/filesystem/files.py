# core:filesystem
from typing import Callable
from pathlib import Path

from geny.core.logger import logger
from geny.core.templates.template import TemplateParser
from geny.core.decorators.error_handler import halt_on_error


class File:
    def __init__(self, name: str, template: str = "", content="", context: dict = None):
        self.context = context if context is not None else {}
        self._name = name
        self._template = template
        self._content = content

    @property
    def name(self) -> str:
        return self._name

    @property
    def template(self) -> str:
        return self._template

    def contents(self, **kwargs) -> str:
        if self.template != "":
            self.context.update(**kwargs)

            content = TemplateParser().parse_file(
                filepath=self.template,
                variables=self.context,
            )

            return content

        content = TemplateParser().parse_string(self._content, variables=self.context)

        return content

    def path(self, parent: Path = None) -> Path:
        value = Path(self.name) if parent is None else parent / self.name
        return value

    @halt_on_error
    def create(self, parent: Path = None, after_hooks: list[Callable] = None, **kwargs):
        if after_hooks is None:
            after_hooks = []

        path = self.path(parent)

        if path.exists():
            if not kwargs.get('GENY_ENABLE_FORCE', False):
                logger.error(f"File already exists: {path}")
                return
            logger.debug(f"Overriding {path}")

        contents = self.contents(**kwargs)

        logger.info(f"create: {path}")

        # NOTE: Handle missing intermediate directories
        if not path.absolute().parent.exists():
            missing = []  # stack up folders that need to be created

            for p in path.parents:
                if not p.exists():
                    missing.insert(0, p)
                    logger.debug(f"Parent directory {p.name} do not exist")

            [p.mkdir(exist_ok=True) for p in missing if len(missing) != 0]

        path.touch(exist_ok=True)

        if contents != "":
            path.write_text(f"{contents}\n")

            logger.debug(f"Add contents to {path.absolute()}")

            [hook(parent, **kwargs) for hook in after_hooks]

    @halt_on_error
    def destroy(
        self, parent: Path = None, after_hooks: list[Callable] = None, **kwargs
    ):
        if after_hooks is None:
            after_hooks = []

        path = self.path(parent)

        logger.info(f"delete: {path}")

        path.unlink(missing_ok=True)

        [hook(parent, **kwargs) for hook in after_hooks]

    def __str__(self) -> str:
        return self.name

    # Implements Sortable

    def __lt__(self, other):
        return self.name < other.name
