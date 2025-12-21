from pathlib import Path

from inflection import underscore, \
    camelize
from jinja2 import Environment, \
    FileSystemLoader

from project_gen.internal.collector import ClientCollector


class Generator:
    def __init__(self):
        self.clients = ClientCollector().collect_clients()
        self.templates_dir = Path(__file__).parent.parent / 'templates' / 'tests'
        self.env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=True)
        self.env.filters["underscore"] = underscore
        self.env.filters["camelize"] = camelize
        self.env.filters["unique_by"] = self.unique_by_filter

    def unique_by_filter(self, items, attribute):
        seen = set()
        unique_items = []
        for item in items:
            key = item.get(attribute)
            if key not in seen:
                seen.add(key)
                unique_items.append(item)
        return unique_items

    def generate(self):
        fixture_template = self.env.get_template("fixtures.jinja2")
        fixtures = fixture_template.render(clients=self.clients)
        with open("clients/fixtures.py", "w", encoding="utf-8") as f:
            f.write(fixtures)

        return fixtures
