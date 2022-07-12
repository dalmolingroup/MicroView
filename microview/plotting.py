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

    common_taxas.update_traces(showlegend=False)

    common_taxas_html = export_to_html(common_taxas, "taxas-plot")

    abund_div = px.scatter(
        tax_data["abund and div"],
        x="Pielou Evenness",
        y="Shannon Diversity",
        size="N Taxas",
        hover_data=["index"],
    )

    abund_div_html = export_to_html(abund_div, "abund-div-plot")

    # Beta diversity plots

    pcoa_embed = (
        tax_data["beta div"].samples[["PC1", "PC2"]].rename_axis("sample").reset_index()
    )
    var_explained = (
        tax_data["beta div"]
        .proportion_explained[:9]
        .to_frame(name="variance explained")
        .reset_index()
        .rename(columns={"index": "PC"})
    )

    pcoa_var = px.line(var_explained, x="PC", y="variance explained", text="PC")
    pcoa_var.update_traces(textposition="bottom right")

    pcoa_var_html = export_to_html(pcoa_var, "pcoa-explained-variance")

    betadiv_pcoa = px.scatter(
        pcoa_embed,
        x="PC1",
        y="PC2",
        hover_data=["sample"],
    )

    betadiv_pcoa_html = export_to_html(betadiv_pcoa, "betadiv_pcoa")

    return {
        "assigned_plot": assigned_html,
        "common_taxas_plot": common_taxas_html,
        "abund_div_plot": abund_div_html,
        "pcoa_var_plot": pcoa_var_html,
        "beta_div_pcoa": betadiv_pcoa_html,
    }
