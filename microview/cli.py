from pathlib import Path

import rich_click as click
from rich.console import Console

from microview import __version__ as mv_version
from microview.file_finder import find_reports
from microview.parse_taxonomy import get_tax_data
from microview.plotting import generate_taxo_plots
from microview.rendering import render_base


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-t",
    "--taxonomy",
    required=True,
    help="Path to taxonomy classification results",
    type=click.Path(),
)
def main(taxonomy: str) -> None:
    console = Console(stderr=True, highlight=False)
    console.print(
        f"\n [bold]Running [blue]Micro[/][red]View[/] :glasses: [dim]v{mv_version}[/] \n"
    )
    reports, report_type = find_reports(Path(taxonomy))
    try:
        console.print(
            f"\n Found [bold]{len(reports)}[/] {report_type.title()} reports... \n"
        )
        tax_results = get_tax_data(reports, report_type)
        tax_plots = generate_taxo_plots(tax_results)
        render_base(tax_plots)
        console.print(f"\n [bold][green]Done![/][/]")
    except Exception:
        console.print("\n An [bold][red]error[/][/] occurred!")
        raise (Exception)
