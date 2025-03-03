# core:filesystem:transformations
import re
from typing import Protocol
from pathlib import Path


class FileTransformation(Protocol):
    def run(self):
        ...


class MoveFile(FileTransformation):
    def __init__(self, file: str, target: str):
        self.file = file
        self.target = target

    def run(self):
        from_ = Path(self.file)
        to_ = Path(self.target)
        from_.rename(to_)


class DeleteFile(FileTransformation):
    def __init__(self, filename: str):
        self.filename = filename

    def run(self):
        file = Path(self.filename)
        file.unlink(missing_ok=True)


class TouchFile(FileTransformation):
    def __init__(self, filename: str):
        self.filename = filename

    def run(self):
        file = Path(self.filename)
        file.touch(exist_ok=True)


class AddLineToFile(FileTransformation):
    def __init__(self, target: Path, statement: str, prevent_duplicates: bool = True):
        self.target = target
        self.statement = statement
        self.prevent_duplicates = prevent_duplicates

    def run(self):
        if self.statement is None or self.statement == "":
            return

        try:
            with open(self.target, mode="r+") as f:
                lines = f.readlines() or []

                if self.prevent_duplicates:
                    for line in lines:
                        # Found a duplicate line. Halt!
                        if line.startswith(self.statement):
                            return

                f.write(f"{self.statement}\n")
        except (FileNotFoundError, OSError) as _:
            pass


class AddImportToFile(AddLineToFile):
    def run(self):
        if self.statement is None or self.statement == "":
            return

        try:
            header_border = 0
            with open(self.target, mode='r+') as f:
                lines = f.readlines() or []

                for idx, line in enumerate(lines):
                    if self.prevent_duplicates and line.startswith(self.statement):
                        return

                    # Matches against comments and import statements
                    if re.match('(^\s+$|^#.*|^"""|^import [a-zA-Z_.]+( as [a-zA-Z_.]+)?(\s+#.*)?$)|(^from [a-zA-Z_.]+ import [a-zA-Z_.]+( as [a-zA-Z_.]+)?(\s+#.*)?$)', line):
                        header_border = idx
                    else:
                        # Found a 'program line'!!
                        break

                # Import statement should go before first 'program line'
                lines.insert(header_border, f"{self.statement}\n\n")

            with open(self.target, 'w') as f:
                f.writelines(lines)
                f.close()
        except (FileNotFoundError, OSError) as _:
            pass


class RemoveLineFromFile(FileTransformation):
    def __init__(self, target: Path, statement: str):
        self.target = target
        self.statement = statement

    def run(self):
        if self.statement is None or self.statement == "":
            return

        try:
            # Find and yank matched line from file
            with open(self.target, mode="r") as f:
                lines = f.readlines()
                for pos, line in enumerate(lines):
                    if line.startswith(self.statement):
                        lines.pop(pos)
                        break

            with open(self.target, mode="w") as f:
                f.writelines(lines)
        except (FileNotFoundError, OSError) as _:
            pass

