from collections import Counter, defaultdict

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
