from pathlib import Path

import rich_click as click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup
from rich.console import Console

from microview import __version__ as mv_version
from microview.file_finder import find_reports, parse_source_table
from microview.parse_taxonomy import get_tax_data
from microview.plotting import generate_taxo_plots
from microview.rendering import render_base


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@optgroup.group(
    "Input data source",
    cls=RequiredMutuallyExclusiveOptionGroup,
    help="Input data source",
)
@optgroup.option(
    "-t",
    "--taxonomy",
    type=click.Path(path_type=Path),
    help="Path to taxonomy classification results",
)
@optgroup.option(
    "-df",
    "--csv-file",
    type=click.Path(path_type=Path),
    help="CSV table with taxonomy classification results paths",
)
def main(taxonomy: Path, csv_file: Path) -> None:
    console = Console(stderr=True, highlight=False)
    console.print(
        f"\n [bold]Running [blue]Micro[/][red]View[/] :glasses: [dim]v{mv_version}[/] \n"
    )
    data_source = taxonomy if taxonomy else csv_file

    if csv_file is not None:
        reports, report_type = parse_source_table(data_source)
    else:
        reports, report_type = find_reports(data_source)

    try:
        console.print(
            f"\n Found [bold]{len(reports)}[/] {report_type.title()} reports... \n"
        )
        tax_results = get_tax_data(reports, report_type)
        tax_plots = generate_taxo_plots(tax_results)
        render_base(tax_plots, data_source)
        console.print(f"\n [bold][green]Done![/][/]")
    except Exception:
        console.print("\n An [bold][red]error[/][/] occurred!")
        raise (Exception)
