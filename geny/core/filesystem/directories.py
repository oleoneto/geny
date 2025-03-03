# core:filesystem
from __future__ import annotations
from typing import Callable
from pathlib import Path
from rich.tree import Tree
from rich.text import Text

from geny.core.logger import logger
from geny.core.filesystem.protocols import FileProtocol
from geny.core.filesystem.files import File
from geny.core.decorators.error_handler import halt_on_error


class Directory:
    def __init__(self, name: str, children: [FileProtocol] = None):
        self.name = name
        self._children = []

        if children is not None:
            self.add_children(children)

    def add_children(self, dirs: list[FileProtocol]):
        dirs = dirs if dirs is not None else []
        [self._children.append(f) for f in dirs]

    @property
    def dirs(self) -> list[Directory]:
        return [f for f in self._children if type(f) is Directory]

    @property
    def files(self) -> list[File]:
        return [f for f in self._children if type(f) is File]

    def print(self, **kwargs):
        """
        A printable representation of the directory structure and its content.
        """
        from rich import print as r

        r(self.tree(**kwargs))

    def tree(self, **kwargs):
        name = Path(self.name)
        tree = Tree(name.__str__())

        for child in sorted(self.dirs):
            child_tree = child.tree(**kwargs)
            if child_tree is None:
                continue
            tree.add(child_tree)

        if kwargs.get("hide_files", False):
            return tree

        for file in sorted(self.files):
            filepath = file.name
            filename = Text(filepath.__str__())
            filename.stylize(f"link file://{filepath}")
            tree.add(filename)

        return tree

    def path(self, parent: Path = None) -> Path:
        if parent is None:
            return Path(self.name)

        if isinstance(parent, str):
            parent = Path(parent)

        return parent / self.name

    @halt_on_error
    def create(self, parent: Path = None, after_hooks: list[Callable] = None, **kwargs):
        if after_hooks is None:
            after_hooks = []

        path = self.path(parent=parent)

        logger.info(f"create: {path.name}")

        path.mkdir(exist_ok=True)

        # Recursively create children items
        for child in self._children:
            child.create(parent=path, **kwargs)

        [hook(parent, **kwargs) for hook in after_hooks]

    @halt_on_error
    def destroy(
        self, parent: Path = None, after_hooks: list[Callable] = None, **kwargs
    ):
        if after_hooks is None:
            after_hooks = []

        path = self.path(parent)

        logger.info(f"delete: {path}")

        for child in self._children:
            child.destroy(parent=path, **kwargs)

        path.rmdir()

        for hook in after_hooks:
            hook(parent, **kwargs)

    def __str__(self) -> str:
        return self.name

    # Implements Sortable

    def __lt__(self, other):
        return self.name < other.name
