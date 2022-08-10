from microview.file_finder import (
    detect_report_type,
    get_validation_dict,
    validate_paths,
)
from microview.schemas import contrast_table_schema


def test_detect_kraken(get_kraken_data):
    kraken_path, report_type = detect_report_type(
        [get_kraken_data], type("test", (), {})()
    )

    assert kraken_path[0] == get_kraken_data
    assert report_type == "kraken"


def test_detect_kaiju(get_kaiju_data):
    kaiju_path, report_type = detect_report_type(
        [get_kaiju_data], type("test", (), {})()
    )

    assert kaiju_path[0] == get_kaiju_data
    assert report_type == "kaiju"


def test_detect_centrifuge(get_centrifuge_data):
    centrifuge_path, report_type = detect_report_type(
        [get_centrifuge_data], type("test", (), {})()
    )

    assert centrifuge_path[0] == get_centrifuge_data
    assert report_type == "kraken"


def test_validate_source_table(get_contrast_data):

    validated = get_validation_dict(get_contrast_data, schema=contrast_table_schema)

    assert validated["errors"] == 0


def test_invalidate_source_table(get_failing_contrast_data):

    validated = get_validation_dict(
        get_failing_contrast_data, schema=contrast_table_schema
    )

    assert validated["errors"] >= 4


def test_path_validation(get_kaiju_data, get_contrast_data):
    full_kaiju = get_kaiju_data.resolve()

    validated = validate_paths([get_kaiju_data], get_contrast_data)

    assert validated[0] == full_kaiju
