import unittest
from tests import parser


class TemplatesTestCase(unittest.TestCase):
    def test_parse_string(self):
        template0 = """# {{ project }}"""
        output = parser.parse_string(template0, {"project": "geny"})
        self.assertEqual(output, "# geny")

        template1 = """My name is {{ name }}"""
        output = parser.parse_string(template1, {"name": "Leo"})
        self.assertEqual(output, "My name is Leo")

        template2 = """My name is {% if name %}{{ name.upper() }}{% else %}Unknown{% endif %}."""
        output = parser.parse_string(template2, {"name": "leo"})
        self.assertEqual(output, "My name is LEO.")

        output = parser.parse_string(template2, variables={})
        self.assertEqual(output, "My name is Unknown.")

    def test_parse_file(self):
        template = "hello.tpl"
        output = parser.parse_file(template, variables={"name": "leo"})
        self.assertEqual(output, "My name is LEO.")

        output = parser.parse_file(template, variables={})
        self.assertEqual(output, "My name is Unknown.")

        template2 = "hello2.tpl"
        output = parser.parse_file(template2, variables={"author": "Leo", "project": "geny"})
        self.assertEqual(output, "# geny\nAuthor: Leo")

        output = parser.parse_file(template2, variables={})
        self.assertEqual(output, "# \n")
