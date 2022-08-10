from pathlib import Path

from click.testing import CliRunner
from microview import cli


def test_with_source_table(get_contrast_data):
    output_path = Path(__file__).parent.resolve() / "test_data" / "table_report.html"

    if output_path.exists():
        output_path.unlink()

    command = f"-df {str(get_contrast_data)} -o {str(output_path)}"

    result = CliRunner().invoke(cli.main, command.split())

    assert result.exit_code == 0
    assert output_path.exists()


def test_with_path(get_contrast_data):
    output_path = Path(__file__).parent.resolve() / "test_data" / "path_report.html"

    if output_path.exists():
        output_path.unlink()

    command = f"-t {str(get_contrast_data.parent)} -o {str(output_path)}"

    result = CliRunner().invoke(cli.main, command.split())

    assert result.exit_code == 0
    assert output_path.exists()


def test_with_failing_table(get_failing_contrast_data):
    output_path = Path(__file__).parent.resolve() / "test_data" / "table_report.html"

    if output_path.exists():
        output_path.unlink()

    command = f"-df {str(get_failing_contrast_data)} -o {str(output_path)}"

    result = CliRunner().invoke(cli.main, command.split())

    assert result.exit_code == 1
    assert output_path.exists() == False
