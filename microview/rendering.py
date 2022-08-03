from datetime import datetime
from pathlib import Path
from typing import Dict

from microview import __version__
from microview.templates import JINJA_ENV


def embed_local_file(filename, filedir="templates"):
    """
    Embed local file into template
    """
    herepath = Path(__file__).parent.resolve()
    fullpath = herepath.joinpath(filedir, filename)

    with open(fullpath, "r") as f:
        return f.read()


def render_base(tax_plots: Dict, dir_path: Path) -> None:
    """
    Render base template

    Args:
        tax_plots (dict): Dict containing results from
            microview.plotting.generate_taxo_plots
        dir_path (Path): Path to directory containing report files
    """
    JINJA_ENV.globals["embed_local_file"] = embed_local_file

    base_template = JINJA_ENV.get_template("base.html")

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
