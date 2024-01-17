# tests
import unittest

from pathlib import Path

from geny.core.templates.template import TemplateParser

parser = TemplateParser(
    templates_dir=[Path(__file__).resolve().parent],
    context={},
)

if __name__ == "__main__":
    unittest.main()
