from datetime import datetime
from pathlib import Path
from typing import Dict

from jinja2 import Environment, PackageLoader

from microview import __version__


def embed_local_file(filename, filedir="templates"):

    herepath = Path(__file__).parent.resolve()
    fullpath = herepath.joinpath(filedir, filename)

    with open(fullpath, "r") as f:
        return f.read()


def render_base(tax_plots: Dict, dir_path: Path) -> None:
    env = Environment(
        loader=PackageLoader("microview", "templates"),
    )

    env.globals["embed_local_file"] = embed_local_file

    base_template = env.get_template("base.html")

    curr_time = datetime.now().strftime("%Y-%m-%d, %H:%M")
    rendered_template = base_template.render(
        tax_plots=tax_plots,
        version=__version__,
        dir_path=str(dir_path.resolve()),
        curr_time=curr_time,
    )
    result_file = Path("microview_report.html").absolute()
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(rendered_template)
