from typing import Dict

import plotly.express as px
from plotly import io
from plotly.graph_objects import Figure


def export_to_html(fig: Figure, div_id: str) -> str:
    return io.to_html(
        fig,
        full_html=False,
        include_plotlyjs=False,
        include_mathjax=False,
        div_id=div_id,
    )


def generate_taxo_plots(tax_data: Dict) -> Dict:

    assigned = px.bar(
        tax_data["sample n reads"], x="index", y="value", color="variable"
    )

    assigned_html = export_to_html(assigned, "assigned-plot")

    common_taxas = px.bar(
        tax_data["common taxas"], x="index", y="value", color="variable"
    )

    common_taxas_html = export_to_html(common_taxas, "taxas-plot")

    abund_div = px.scatter(
        tax_data["abund and div"],
        x="Pielou Evenness",
        y="Shannon Diversity",
        hover_data=["index"],
    )

    abund_div_html = export_to_html(abund_div, "abund-div-plot")

    return {
        "assigned_plot": assigned_html,
        "common_taxas_plot": common_taxas_html,
        "abund_div_plot": abund_div_html,
    }
