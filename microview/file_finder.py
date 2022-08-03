from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from frictionless import checks, validate

from microview.schemas import contrast_table_schema, kaiju_report_schema


def validate_against_schema(table: Path, **kwargs) -> Dict:

    report = validate(
        table,
        **kwargs,
    )

    return {
        "report": table,
        "errors": report["stats"]["errors"],
        "error_messages": report.flatten(["code", "message"]),
    }


def is_kraken_report(report: Dict) -> bool:
    if report["errors"] == 0 or all(
        report_error[0] == "duplicate-label"
        for report_error in report["error_messages"]
    ):
        return True
    return False


def check_source_table_validation(report: Dict, console) -> None:

    if report["errors"] > 0:
        console.print(
            " [bold]Source table does not follow expected 'sample,group' schema\n"
            " See the following errors raised during validation:[/]"
        )
        for error in report["error_messages"]:
            console.print(f" [red][bold]{error[0]}[/]: {error[1]}[/]")
        raise Exception("Source table does not follow schema")


def detect_report_type(report_paths: List[Path], console) -> Tuple[List[Path], str]:

    kaiju_validated = [
        validate_against_schema(report, schema=kaiju_report_schema)
        for report in report_paths
    ]
    kaiju_reports = [
        kaiju_report["report"]
        for kaiju_report in kaiju_validated
        if kaiju_report["errors"] == 0
    ]
    if len(kaiju_reports) == 0:

        # TODO: Improve Kraken validation
        kraken_validated = [
            validate_against_schema(
                report, checks=[checks.table_dimensions(num_fields=6)]
            )
            for report in report_paths
        ]
        kraken_reports = [
            kraken_report["report"]
            for kraken_report in kraken_validated
            if is_kraken_report(kraken_report)
        ]

        if len(kraken_reports) == 0:
            console.print("\n [red]Could not find any valid reports[/]")
            raise Exception("Could not find any valid files.")
        else:
            report_type = "kraken"
            return kraken_reports, report_type
    else:
        report_type = "kaiju"
        return kaiju_reports, report_type


def find_reports(reports_path: Path, console) -> Tuple[List[Path], str]:
    file_paths: List[Path] = list(reports_path.glob("*tsv"))
    report_paths, report_type = detect_report_type(file_paths, console)
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

    report = validate_against_schema(source_table, schema=contrast_table_schema)

    check_source_table_validation(report, console)

    df = pd.read_csv(source_table)

    sample_paths: List[Path] = [Path(sample) for sample in df["sample"].to_list()]

    validated_paths = validate_paths(sample_paths, source_table)

    report_paths, report_type = detect_report_type(validated_paths, console)

    return {
        "paths": report_paths,
        "report_type": report_type,
        "dataframe": df,
    }
