import unittest
from pathlib import Path
from click.testing import CliRunner

from geny.core.filesystem.transformations import (
    DeleteFile,
    MoveFile,
    AddLineToFile,
    AddImportToFile,
    RemoveLineFromFile,
)

runner = CliRunner()


class TransformationsTestCase(unittest.TestCase):
    def test_add_line(self):
        file = Path("new.scratch")

        with runner.isolated_filesystem():
            file.write_text("line_1\n")

            AddLineToFile(file, "line_2").run()
            self.assertEqual("line_1\nline_2\n", file.read_text("utf-8"))

            AddLineToFile(file, "line_3").run()
            self.assertEqual("line_1\nline_2\nline_3\n", file.read_text("utf-8"))

    def test_add_import_line(self):
        file = Path("new.scratch")

        with runner.isolated_filesystem():
            file.write_text("""
# example
import sys
import math
import random
import numpy as np # used for matrix stuff


from django.db import models # TODO: work with models
# from pathlib import Path

# TODO: implement
def main():
    return "greetings"

if __name__ == "__main__":
    from pprint import pprint as p
    p(main())
""")

            stmt = "from os import listdir as ls"
            AddImportToFile(file, stmt).run()
            self.assertIn("from os import listdir as ls", file.read_text("utf-8"))

            with open(file, 'r') as f:
                lines = f.readlines()

                # import statement
                self.assertIn(stmt, lines[11])

                # surrounding lines (before and after)
                self.assertIn("# from pathlib import Path", lines[9])
                self.assertIn("# TODO: implement", lines[13])


    def test_remove_line(self):
        file = Path("new.scratch")

        with runner.isolated_filesystem():
            file.write_text("line_1\nline_2\n")

            # Do nothing
            RemoveLineFromFile(file, "line_3").run()
            self.assertEqual("line_1\nline_2\n", file.read_text("utf-8"))

            # Pop string
            RemoveLineFromFile(file, "line_1").run()
            self.assertEqual("line_2\n", file.read_text("utf-8"))

    def test_move_file(self):
        source = "file.py"
        target = "new.py"

        with runner.isolated_filesystem():
            Path(source).touch()
            Path(target).touch()

            self.assertTrue(Path(source).exists())
            self.assertTrue(Path(target).exists())

            MoveFile(source, target).run()

            self.assertFalse(Path(source).exists())
            self.assertTrue(Path(target).exists())

    def test_delete_file(self):
        source = "file.py"
        file = Path(source)

        with runner.isolated_filesystem():
            file.touch()
            self.assertTrue(file.exists())

            DeleteFile(source).run()

            self.assertFalse(file.exists())
