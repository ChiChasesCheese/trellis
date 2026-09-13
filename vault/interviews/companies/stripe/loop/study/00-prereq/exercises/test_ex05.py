"""ex05 测试。运行：python -m pytest test_ex05.py -q"""

CSV_TEXT = (
    "id,name,city,amount\n"
    '1,"Alpha, Inc.",SF,100\n'  # 带引号且内含逗号的字段
    "2,Beta,NY,50\n"
    ",Gamma,LA,10\n"  # 缺 id -> 跳过
    "4,Delta,SEA,oops\n"  # amount 解析失败 -> 跳过
)


def test_read_csv_text_parses_by_name_and_handles_quoted_comma(ex):
    rows = ex.read_csv_text(CSV_TEXT)
    assert rows == [
        {"id": "1", "name": "Alpha, Inc.", "city": "SF", "amount": 100},
        {"id": "2", "name": "Beta", "city": "NY", "amount": 50},
    ]


def test_read_csv_text_column_order_does_not_matter(ex):
    reordered = "city,amount,id,name\nSF,100,1,Alpha\n"
    rows = ex.read_csv_text(reordered)
    assert rows == [{"city": "SF", "amount": 100, "id": "1", "name": "Alpha"}]


def test_read_csv_text_empty_string_is_empty_list(ex):
    assert ex.read_csv_text("") == []


def test_write_csv_rows_quotes_comma_and_uses_lf(ex):
    out = ex.write_csv_rows([{"name": "Alpha, Inc.", "total": 100}], ["name", "total"])
    assert "\r\n" not in out
    assert out == 'name,total\n"Alpha, Inc.",100\n'


def test_write_csv_rows_empty_rows_still_has_header(ex):
    out = ex.write_csv_rows([], ["a", "b"])
    assert out == "a,b\n"


def test_clean_numeric_rows_splits_ok_and_bad(ex):
    rows = [{"id": "1", "amount": "100"}, {"id": "2", "amount": "oops"}, {"id": "3", "amount": "50"}]
    ok, bad = ex.clean_numeric_rows(rows, "amount")
    assert ok == [{"id": "1", "amount": 100}, {"id": "3", "amount": 50}]
    assert bad == [{"id": "2", "amount": "oops"}]


def test_clean_numeric_rows_missing_field_counts_as_bad(ex):
    ok, bad = ex.clean_numeric_rows([{"id": "1"}], "amount")
    assert ok == []
    assert bad == [{"id": "1"}]


def test_clean_numeric_rows_empty_input(ex):
    assert ex.clean_numeric_rows([], "amount") == ([], [])


def test_parse_events_jsonl_skips_blank_and_bad_lines(ex):
    text = '{"a": 1}\n\n   \nnot json\n{"a": 2}\n'
    assert ex.parse_events_jsonl(text) == [{"a": 1}, {"a": 2}]


def test_parse_events_jsonl_empty_text(ex):
    assert ex.parse_events_jsonl("") == []


def test_dig_walks_nested_dict_and_list(ex):
    obj = {"charges": {"data": [{"amount": 100}, {"amount": 200}]}}
    assert ex.dig(obj, "charges", "data", 0, "amount") == 100
    assert ex.dig(obj, "charges", "data", 1, "amount") == 200


def test_dig_returns_default_on_missing_or_none(ex):
    obj = {"a": {"b": None}}
    assert ex.dig(obj, "a", "b", "c", default="X") == "X"
    assert ex.dig(obj, "a", "missing", default=0) == 0
    assert ex.dig(obj, "a", "b", 3, default=-1) == -1  # 中途是 None，不能再往里挖


def test_dig_wrong_container_type_returns_default(ex):
    obj = {"a": [1, 2, 3]}
    assert ex.dig(obj, "a", "not_an_index", default="fallback") == "fallback"


def test_field_status_distinguishes_missing_null_present(ex):
    d = {"a": 1, "b": None}
    assert ex.field_status(d, "a") == "present"
    assert ex.field_status(d, "b") == "null"
    assert ex.field_status(d, "c") == "missing"


def test_field_status_empty_dict_is_missing(ex):
    assert ex.field_status({}, "anything") == "missing"


def test_sum_amounts_decimal_avoids_float_drift(ex):
    # float(0.1) + float(0.2) != 0.3 —— Decimal(str(v)) 才是精确的
    assert (0.1 + 0.2) != 0.3
    assert ex.sum_amounts_decimal([0.1, 0.2]) == "0.3"


def test_sum_amounts_decimal_mixed_types(ex):
    assert ex.sum_amounts_decimal([100, "50", 0.25]) == "150.25"


def test_sum_amounts_decimal_empty_is_zero(ex):
    assert ex.sum_amounts_decimal([]) == "0"


def test_summarize_list_response_normal(ex):
    body = {"object": "list", "data": [{"id": "ch_1", "amount": 100}, {"id": "ch_2", "amount": 250}]}
    assert ex.summarize_list_response(body) == (350, "ch_2")


def test_summarize_list_response_error_body(ex):
    body = {"error": {"type": "invalid_request_error", "message": "nope"}}
    assert ex.summarize_list_response(body) == (0, None)


def test_summarize_list_response_empty_data(ex):
    assert ex.summarize_list_response({"object": "list", "data": []}) == (0, None)


def test_csv_to_grouped_report_full_pipeline(ex):
    text = "merchant,amount\nm_a,100\nm_b,50\nm_a,25\n"
    out = ex.csv_to_grouped_report(text, "merchant", "amount")
    assert out == '{"m_a": "125", "m_b": "50"}'


def test_csv_to_grouped_report_skips_dirty_rows(ex):
    text = "merchant,amount\nm_a,100\n,999\nm_a,oops\nm_b,10\n"
    out = ex.csv_to_grouped_report(text, "merchant", "amount")
    assert out == '{"m_a": "100", "m_b": "10"}'


def test_csv_to_grouped_report_output_is_stable_json_sorted(ex):
    text = "merchant,amount\nz_last,1\na_first,2\n"
    out = ex.csv_to_grouped_report(text, "merchant", "amount")
    assert out.index('"a_first"') < out.index('"z_last"')
