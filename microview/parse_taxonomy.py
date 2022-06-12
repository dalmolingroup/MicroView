from collections import Counter
from pathlib import Path
from typing import Counter, Dict, List, Tuple

import numpy as np
import pandas as pd
from skbio.diversity import alpha_diversity


def parse_kaiju2table(files: List[Path]) -> dict:
    parsed_stats: Dict[str, dict] = {}

    for sample in files:
        df = pd.read_table(sample).replace({"None": np.NaN}, regex=True)

        sample_name = sample.name
        parsed_stats[sample_name] = {"assigned": {}}

        for row in df.itertuples():

            row_dict = {"n_reads": row.reads, "percent": row.percent}
            if row.taxon_name == "unclassified":
                parsed_stats[sample_name]["unclassified"] = row_dict
            elif row.taxon_name.startswith("cannot"):
                parsed_stats[sample_name]["cannot be assigned"] = row_dict
            else:
                taxon_name: str = list(filter(None, row.taxon_name.split(";")))[-1]
                parsed_stats[sample_name]["assigned"][taxon_name] = row_dict

    return parsed_stats


def get_taxon_counts(samples_stats) -> Tuple[dict, dict]:
    all_sample_counts: Dict = {}

    for sample, data in samples_stats.items():
        all_sample_counts[sample] = Counter()
        for category, cat_data in data.items():
            if category == "assigned":
                for tax_name, info in cat_data.items():
                    all_sample_counts[sample][tax_name] += info["n_reads"]
            else:
                all_sample_counts[sample][category] += cat_data["n_reads"]

    return all_sample_counts


def build_taxonomy_stats(parsed_stats: Dict) -> Dict:
    results: Dict[str, dict] = {}
    for sample_name, _ in parsed_stats.items():
        results[sample_name] = {"assigned": 0, "unassigned": 0}
        assigned = sum(
            d["n_reads"] for d in parsed_stats[sample_name]["assigned"].values()
        )

        unassigned = (
            parsed_stats[sample_name]["cannot be assigned"]["n_reads"]
            + parsed_stats[sample_name]["unclassified"]["n_reads"]
        )

        total = assigned + unassigned
        results[sample_name]["assigned"] = (assigned / total) * 100
        results[sample_name]["unassigned"] = (unassigned / total) * 100

    return results


def get_common_taxas(sample_counts: Dict) -> Dict:
    most_common: Dict = {}
    for sample in sample_counts.keys():
        sample_total = sample_counts[sample].total()
        most_common_vals = sample_counts[sample].most_common(7)
        other = sample_total - sum(v for _, v in most_common_vals)
        most_common[sample] = {k: (v / sample_total) * 100 for k, v in most_common_vals}
        most_common[sample]["other"] = (other / sample_total) * 100
    return most_common


def calculate_abund_diver(sample_counts: Dict) -> pd.DataFrame:
    taxa_counts_df = pd.DataFrame(sample_counts).T.fillna(0)
    ids = taxa_counts_df.index

    shannon_div = alpha_diversity("shannon", taxa_counts_df.to_numpy(), ids)

    div_abund_df = pd.DataFrame(
        shannon_div, columns=["Shannon Diversity"]
    ).reset_index()

    div_abund_df["taxa_n"] = np.count_nonzero(taxa_counts_df.to_numpy(), axis=1)

    # Pielou's evenness = diversity divided by the log specnumber
    div_abund_df["Pielou Evenness"] = div_abund_df["Shannon Diversity"] / np.log(
        div_abund_df["taxa_n"]
    )

    return div_abund_df


def get_tax_data(paths: List[Path]) -> Dict:

    parsed_stats = parse_kaiju2table(paths)

    all_sample_counts = get_taxon_counts(parsed_stats)

    n_reads = build_taxonomy_stats(parsed_stats)

    most_common = get_common_taxas(all_sample_counts)

    abund_div_df = calculate_abund_diver(all_sample_counts)

    stats_df = pd.DataFrame(n_reads).T.reset_index().melt(id_vars=["index"])

    most_common_df = (
        pd.DataFrame.from_dict(most_common, orient="index")
        .reset_index()
        .melt(id_vars=["index"])
    )

    return {
        "sample n reads": stats_df,
        "common taxas": most_common_df,
        "abund and div": abund_div_df,
    }
