from pathlib import Path
from typing import List, Tuple


def find_reports(reports_path: Path) -> Tuple[List[Path], str]:
    report_paths: List[Path] = list(reports_path.glob("*tsv"))
    report_type = "kraken"
    if all("kaiju" in path.name for path in report_paths):
        report_type = "kaiju"
    return report_paths, report_type
