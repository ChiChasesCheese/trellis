import pytest

from filevault.store import Where


def test_empty_where():
    assert Where().build() == ("", ())


def test_conditions_are_anded_and_parameterised():
    sql, params = Where().eq("owner", "x' OR '1'='1").compare("size", ">=", 10).build()
    assert sql == "WHERE owner = ? AND size >= ?"
    assert params == ("x' OR '1'='1", 10)


def test_row_compare():
    sql, params = Where().row_compare(("created_at", "id"), "<", ("t", "i")).build()
    assert sql == "WHERE (created_at, id) < (?, ?)"
    assert params == ("t", "i")


@pytest.mark.parametrize("column", ["owner; DROP TABLE files", "nope", ""])
def test_unknown_columns_are_rejected(column):
    with pytest.raises(ValueError):
        Where().eq(column, 1)


def test_unknown_operator_is_rejected():
    with pytest.raises(ValueError):
        Where().compare("size", "; --", 1)


def test_contains_is_case_insensitive_and_escapes_wildcards():
    sql, params = Where().contains("filename", "100%_Done").build()
    assert sql == "WHERE LOWER(filename) LIKE ? ESCAPE '\\'"
    assert params == ("%100\\%\\_done%",)
