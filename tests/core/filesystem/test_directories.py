import os
import unittest
from click.testing import CliRunner

from geny.core.filesystem.directories import Directory, File


runner = CliRunner()


class DirectoryTestCase(unittest.TestCase):
    def test_create_empty_directory(self):
        with runner.isolated_filesystem():
            d = Directory("project")
            d.create()

            self.assertTrue(d.path().exists())
            self.assertTrue(d.path().is_dir())

            self.assertEqual(0, len(d.dirs))
            self.assertEqual(0, len(d.files))

    def test_create_directory_with_files(self):
        with runner.isolated_filesystem():
            name = "project"

            d = Directory(
                name,
                children=[
                    File(name="file1.txt"),
                    File(name="file2.md", template="# {{ name }}"),
                    Directory("folder"),
                ],
            )

            d.create(**{"name": "Bookstore"})

            self.assertTrue(d.path().exists())
            self.assertTrue(d.path().is_dir())

            # Sub-directories
            self.assertEqual(1, len(d.dirs))
            self.assertEqual("folder", d.dirs[0].name)
            self.assertTrue(d.dirs[0].path(d.path()).exists())

            # Files
            self.assertEqual(2, len(d.files))
            self.assertEqual("file1.txt", d.files[0].name)
            self.assertEqual("file2.md", d.files[1].name)

            for file in d.files:
                self.assertTrue(file.path(d.path()).exists())
                self.assertTrue(file.path(d.path()).is_file())

            self.assertEqual("# Bookstore\n", d.files[1].path(d.path()).read_text())

    def test_create_directory_with_template_files(self):
        with runner.isolated_filesystem():
            parent = "project"
            file1 = File(name="file1.txt", content="File 1")
            file2 = File(name="file2.md", content="File 2")
            dir1 = Directory("folder")

            d = Directory(
                parent,
                children=[
                    file1,
                    file2,
                    dir1,
                ],
            )

            d.create()

            self.assertTrue(d.path().exists())
            self.assertTrue(d.path().is_dir())

            self.assertEqual(1, len(d.dirs))
            self.assertEqual(2, len(d.files))

            self.assertEqual("folder", d.dirs[0].name)
            self.assertEqual(file1, d.files[0])
            self.assertEqual(file2, d.files[1])

            self.assertEqual(sorted([file1.name, dir1.name, file2.name]), sorted(os.listdir(parent)))

            self.assertEqual("File 1\n", file1.path(parent=d.path()).read_text())
            self.assertEqual("File 2\n", file2.path(parent=d.path()).read_text())

    def test_delete_directory(self):
        with runner.isolated_filesystem():
            name = "project"

            d = Directory(
                name,
                children=[
                    File(name="file1.txt"),
                    File(name="file2.md"),
                    Directory("folder"),
                ],
            )

            d.create()

            self.assertTrue(d.path().exists())
            self.assertTrue(d.path().is_dir())

            d.destroy()

            self.assertFalse(d.path().exists())
