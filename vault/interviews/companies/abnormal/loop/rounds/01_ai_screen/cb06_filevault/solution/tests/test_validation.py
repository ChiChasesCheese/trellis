import pytest

from filevault.errors import InvalidInput
from filevault.validation import clean_content_type, clean_filename


def test_filename_is_trimmed():
    assert clean_filename("  a.txt ") == "a.txt"


@pytest.mark.parametrize("bad", ["", "  ", "a/b", "a\\b", "a\x00b", "x" * 256])
def test_bad_filenames(bad):
    with pytest.raises(InvalidInput):
        clean_filename(bad)


def test_unicode_and_quotes_are_fine():
    assert clean_filename("报告 'final' (2).pdf") == "报告 'final' (2).pdf"


def test_content_type_defaults_and_validates():
    assert clean_content_type(None) == "application/octet-stream"
    assert clean_content_type("  ") == "application/octet-stream"
    assert clean_content_type("text/plain; charset=utf-8") == "text/plain; charset=utf-8"
    with pytest.raises(InvalidInput):
        clean_content_type("plain")


def test_parse_filters_reads_every_parameter():
    from datetime import datetime, timezone

    from filevault.validation import parse_filters

    f = parse_filters(
        {"q": " Report ", "type": "application/pdf", "min_size": "10", "max_size": "20",
         "from": "2026-09-01", "to": "2026-09-02T12:30:00Z"}
    )
    assert (f.q, f.content_type, f.min_size, f.max_size) == ("Report", "application/pdf", 10, 20)
    assert f.created_from == datetime(2026, 9, 1, tzinfo=timezone.utc)
    assert f.created_to == datetime(2026, 9, 2, 12, 30, tzinfo=timezone.utc)


def test_parse_filters_ignores_blank_values():
    from filevault.validation import parse_filters

    f = parse_filters({"q": "", "min_size": "", "from": None})
    assert f.q is None and f.min_size is None and f.created_from is None


@pytest.mark.parametrize(
    "raw, field",
    [
        ({"min_size": "ten"}, "min_size"),
        ({"max_size": "-1"}, "max_size"),
        ({"min_size": "5", "max_size": "4"}, "min_size"),
        ({"from": "yesterday"}, "from"),
        ({"to": "2026-13-45"}, "to"),
        ({"from": "2026-09-02", "to": "2026-09-01"}, "from"),
    ],
)
def test_parse_filters_names_the_bad_parameter(raw, field):
    from filevault.validation import parse_filters

    with pytest.raises(InvalidInput) as err:
        parse_filters(raw)
    assert err.value.field == field
