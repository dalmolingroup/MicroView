from pathlib import Path
from typing import List


def find_kaiju_reports(reports_path: Path) -> List[Path]:
    report_paths: List[Path] = reports_path.glob("*_kaiju.tsv")
    return list(report_paths)
