from pathlib import Path
from typing import List, Tuple

import pandas as pd


def detect_report_type(report_paths: List[Path]) -> str:
    report_type = "kraken"
    if all("kaiju" in path.name for path in report_paths):
        report_type = "kaiju"

    return report_type


def find_reports(reports_path: Path) -> Tuple[List[Path], str]:
    report_paths: List[Path] = list(reports_path.glob("*tsv"))
    report_type = detect_report_type(report_paths)
    return report_paths, report_type


def validate_paths(sample_paths: List[Path], source_table: Path) -> List[Path]:

    if all(sample_path.exists for sample_path in sample_paths) != True:
        full_sample_paths: List[Path] = [
            source_table.parent.joinpath(sample) for sample in sample_paths
        ]

        if all(full_path.exists() for full_path in full_sample_paths) != True:
            raise Exception("One or more provided sample paths doesn't exist")

        return full_sample_paths

    return sample_paths


def parse_source_table(source_table: Path) -> Tuple[List[Path], str]:

    df = pd.read_csv(source_table)

    sample_paths: List[Path] = [Path(sample) for sample in df["sample"].to_list()]

    report_type = detect_report_type(sample_paths)

    validated_paths = validate_paths(sample_paths, source_table)

    return validated_paths, report_type
