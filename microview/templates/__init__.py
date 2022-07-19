from pathlib import Path

from jinja2 import Environment, FileSystemLoader

HERE = Path(__file__).parent.resolve()

JINJA_ENV = Environment(
    loader=FileSystemLoader(str(HERE)),
)
