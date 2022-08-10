from collections import Counter, defaultdict
from pathlib import Path

import pytest


@pytest.fixture
def parsed_stats():
    sample_stats = {
        "sample1": defaultdict(
            lambda: {"n_reads": 0, "percent": 0},
            {"assigned": {"tax1": {"n_reads": 5, "percent": 1}}},
        ),
        "sample2": defaultdict(
            lambda: {"n_reads": 0, "percent": 0},
            {
                "assigned": {
                    "tax1": {"n_reads": 5, "percent": 0.33},
                    "tax2": {"n_reads": 10, "percent": 0.66},
                },
                "unclassified": {"n_reads": 1, "percent": 0.01},
            },
        ),
    }

    return sample_stats


@pytest.fixture
def all_sample_counts():
    counts = {
        "sample1": Counter({"tax1": 5}),
        "sample2": Counter({"tax1": 5, "tax2": 10}),
    }

    return counts


@pytest.fixture
def get_kraken_data():
    return Path(__file__).parent.resolve() / "test_data" / "kraken_test.tsv"


@pytest.fixture
def get_kaiju_data():
    return Path(__file__).parent.resolve() / "test_data" / "kaiju_test.tsv"


@pytest.fixture
def get_centrifuge_data():
    return Path(__file__).parent.resolve() / "test_data" / "centrifuge_test.tsv"


@pytest.fixture
def get_contrast_data():
    return Path(__file__).parent.resolve() / "test_data" / "contrast_table.csv"


@pytest.fixture
def get_failing_contrast_data():
    return Path(__file__).parent.resolve() / "test_data" / "contrast_table_failing.csv"
