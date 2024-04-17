# core:templates
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from geny.core.decorators.singleton import singleton
from geny.core.templates.protocols import TemplateParserProtocol


@singleton
class TemplateParser(TemplateParserProtocol):
    def __init__(self, templates_dir: list[Path] = None, context: dict = None):
        if context is None:
            context = {}

        if templates_dir is None:
            templates_dir = []

        self.project = context.get("project", "")
        self.app = context.get("app", "")
        self.context = context
        self.templates = templates_dir

    def parse_file(self, filepath, variables, templates: list[Path] = None) -> str:
        variables.update(self.context)

        if templates is not None:
            self.templates = templates + self.templates

        environment = Environment(
            loader=FileSystemLoader(self.templates),
            autoescape=select_autoescape(),
        )

        return environment.get_template(filepath).render(variables)

    def parse_string(self, content, variables) -> str:
        variables.update(self.context)

        environment = Environment(autoescape=select_autoescape()).from_string(content)
        return environment.render(variables)
