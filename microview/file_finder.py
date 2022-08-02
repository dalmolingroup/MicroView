from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from frictionless import validate

from microview.schemas import contrast_table_schema


def validate_against_schema(table: Path, schema: Path) -> Dict:

    report = validate(
        table,
        schema=schema,
    )

    return {
        "errors": report["stats"]["errors"],
        "error_messages": report.flatten(["code", "message"]),
    }


def check_source_table_validation(report: Dict, console) -> bool:

    if report["errors"] > 0:
        console.print(
            " [bold]Source table does not follow expected 'sample,group' schema\n"
            " See the following errors raised during validation:[/]"
        )
        for error in report["error_messages"]:
            console.print(f" [red][bold]{error[0]}[/]: {error[1]}[/]")
        raise Exception("Source table does not follow schema")


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


def parse_source_table(source_table: Path, console) -> Dict:

    report = validate_against_schema(source_table, contrast_table_schema)

    check_source_table_validation(report, console)

    df = pd.read_csv(source_table)

    sample_paths: List[Path] = [Path(sample) for sample in df["sample"].to_list()]

    report_type = detect_report_type(sample_paths)

    validated_paths = validate_paths(sample_paths, source_table)

    return {
        "paths": validated_paths,
        "report_type": report_type,
        "dataframe": df,
    }
