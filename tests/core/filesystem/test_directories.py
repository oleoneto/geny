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
                ],
            )

            d.create(**{"name": "Bookstore"})

            self.assertEqual(0, len(d.dirs))

            # Files
            self.assertEqual(2, len(d.files))
            self.assertEqual("file1.txt", d.files[0].name)
            self.assertEqual("file2.md", d.files[1].name)

            for file in d.files:
                self.assertTrue(file.path(d.path()).exists())
                self.assertTrue(file.path(d.path()).is_file())

            self.assertEqual("# Bookstore\n", d.files[1].path(d.path()).read_text())

    def test_create_directory_with_mixed_contents(self):
        with runner.isolated_filesystem():
            name = "project"

            """
            project/
                src/
                    main.py
                    utils/
                        __init__.py
            """
            d = Directory(
                name,
                children=[
                    File(name="README.md", template="# {{ project_name }}"),
                    Directory(
                        "src",
                        children=[
                            File(name="main.py", template="def {{ func_name }}():\n\tpass"),
                            Directory("utils", children=[File(name="__init__.py", template="# {{ project_name }}.src.utils")])
                        ],
                  ),
                ],
            )

            d.create(**{"project_name": "click", "func_name": "main"})

            self.assertTrue(d.path().exists())
            self.assertTrue(d.path().is_dir())

            # Files
            self.assertEqual(1, len(d.files))
            self.assertEqual("README.md", d.files[0].name)

            ### Sub-directories ###

            # Dir: project/src/
            source_dir = d.dirs[0].path(d.path())

            self.assertEqual(1, len(d.dirs))
            self.assertTrue(source_dir.exists())

            self.assertEqual("src", d.dirs[0].name)
            self.assertTrue(source_dir.is_dir())
            self.assertEqual(1, len(d.dirs[0].dirs))
            self.assertEqual(1, len(d.dirs[0].files))

            # File: project/src/main.py
            self.assertEqual("main.py", d.dirs[0].files[0].name)
            self.assertTrue(d.dirs[0].files[0].path(source_dir).exists())
            self.assertTrue(d.dirs[0].files[0].path(source_dir).is_file())
            self.assertEqual("def main():\n\tpass\n", d.dirs[0].files[0].path(source_dir).read_text())

            # Dir: project/src/utils/
            utils_dir = d.dirs[0].dirs[0].path(source_dir)

            self.assertEqual("utils", d.dirs[0].dirs[0].name)
            self.assertEqual(1, len(d.dirs[0].dirs))
            self.assertEqual(1, len(d.dirs[0].files))
            self.assertTrue(d.dirs[0].dirs[0].path(source_dir).exists())
            self.assertTrue(d.dirs[0].dirs[0].path(source_dir).is_dir())
            self.assertTrue(d.dirs[0].files[0].path(source_dir).exists())
            self.assertTrue(d.dirs[0].files[0].path(source_dir).is_file())

            # File: project/src/utils/__init__.py
            self.assertEqual("__init__.py", d.dirs[0].dirs[0].files[0].name)
            self.assertTrue(d.dirs[0].dirs[0].files[0].path(utils_dir).exists())
            self.assertTrue(d.dirs[0].dirs[0].files[0].path(utils_dir).is_file())
            self.assertEqual("# click.src.utils\n", d.dirs[0].dirs[0].files[0].path(utils_dir).read_text())

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
