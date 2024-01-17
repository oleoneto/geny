# core:filesystem
from pathlib import Path
from typing import Callable, Protocol


class FinderProtocol(Protocol):
    def find(self, path: Path, patterns: list[str]) -> dict:
        ...


class FileProtocol(Protocol):
    def create(self, parent: Path, after_hooks: list[Callable], **kwargs):
        ...

    def destroy(self, parent: Path, after_hooks: list[Callable], **kwargs):
        ...

    def path(self, parent: Path) -> Path:
        ...
