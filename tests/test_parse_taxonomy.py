from ctypes import resize
from random import sample

from microview.parse_taxonomy import (
    build_taxonomy_stats,
    calculate_abund_diver,
    get_common_taxas,
    get_taxon_counts,
)


def test_get_taxon_counts(parsed_stats):

    results = get_taxon_counts(parsed_stats)

    assert results["sample1"]["tax1"] == 5
    assert results["sample2"]["tax2"] == 10


def test_build_taxonomy_stats(parsed_stats):

    n_reads = build_taxonomy_stats(parsed_stats)

    assert n_reads["sample2"]["assigned"] == 93.75
    assert n_reads["sample2"]["unassigned"] == 6.25


def test_get_common_taxas(all_sample_counts):

    most_common = get_common_taxas(all_sample_counts)

    assert most_common["sample2"]["tax2"] == 66.67


def test_calculate_abund_diver(all_sample_counts):

    abund_div_df = calculate_abund_diver(all_sample_counts)

    assert round(abund_div_df[0]["Shannon Diversity"][1], 2) == 0.92
