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
