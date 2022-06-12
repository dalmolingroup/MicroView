from pathlib import Path

import rich_click as click

from microview.parse_taxonomy import get_tax_data
from microview.plotting import generate_taxo_plots
from microview.rendering import render_base


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--taxonomy",
    required=True,
    help="Path to taxonomy classification results",
    type=click.Path(),
)
def main(taxonomy: Path) -> None:
    tax_results = get_tax_data(taxonomy)
    tax_plots = generate_taxo_plots(tax_results)
    render_base(tax_plots)
