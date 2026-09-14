"""ex04 测试。运行：python -m pytest test_ex04.py -q"""


def test_split_command_and_rest_only_splits_first_comma(ex):
    got = ex.split_command_and_rest("SET_LIMIT, acct_9, 5000")
    assert got == ("SET_LIMIT", "acct_9, 5000"), (
        f"得到 {got!r}——rest 里应该还留着第二个逗号，maxsplit=1 只切第一刀"
    )


def test_split_command_and_rest_no_comma_and_dirty_spacing(ex):
    assert ex.split_command_and_rest("PING") == ("PING", "")
    assert ex.split_command_and_rest("  REFUND , ch_1,500  ") == ("REFUND", "ch_1,500")


def test_last_resource_id_takes_last_segment(ex):
    assert ex.last_resource_id("acct_9/charges/ch_1") == "ch_1"
    assert ex.last_resource_id("a/b/c/d") == "d"


def test_last_resource_id_no_separator_and_whitespace(ex):
    assert ex.last_resource_id("ch_1") == "ch_1"
    assert ex.last_resource_id("  acct_9/ch_2 ") == "ch_2"


def test_to_cents_matches_worked_examples(ex):
    assert ex.to_cents("12.5") == 1250
    assert ex.to_cents("-0.05") == -5
    assert ex.to_cents("7") == 700


def test_to_cents_whitespace_and_truncates_extra_digits(ex):
    assert ex.to_cents("  -3.4 ") == -340
    assert ex.to_cents("0") == 0
    assert ex.to_cents("10.999") == 1099, "分只取小数点后两位，多出来的截断，不四舍五入"


def test_fmt_cents_matches_worked_examples(ex):
    assert ex.fmt_cents(1250) == "12.50"
    assert ex.fmt_cents(-5) == "-0.05"
    assert ex.fmt_cents(0) == "0.00"


def test_fmt_cents_small_value_still_two_digits(ex):
    assert ex.fmt_cents(5) == "0.05"


def test_format_fee_line_is_byte_exact(ex):
    got = ex.format_fee_line("m_a", 2.5, 1250, width=6)
    assert got == "   m_a | fee 2.50% | amount 12.50", f"得到 {got!r}——逐字符对比宽度和小数位"


def test_format_fee_line_handles_negative_values(ex):
    got = ex.format_fee_line("m_b", -1.5, -250, width=5)
    assert got == "  m_b | fee -1.50% | amount -2.50"


def test_normalize_merchant_name_matches_worked_example(ex):
    assert ex.normalize_merchant_name("  Alpha   INC. ") == "alpha inc"


def test_normalize_merchant_name_tabs_and_multiple_trailing_dots(ex):
    assert ex.normalize_merchant_name("\tGamma Co.\n") == "gamma co"
    assert ex.normalize_merchant_name("Delta Corp..") == "delta corp"


def test_parse_accept_language_matches_worked_example(ex):
    got = ex.parse_accept_language("en-US, fr;q=0.8 , *;q=0.1")
    assert got == [("en-US", 1.0), ("fr", 0.8), ("*", 0.1)]


def test_parse_accept_language_missing_and_bad_q_default_to_one(ex):
    assert ex.parse_accept_language("en-US;q=oops, fr") == [("en-US", 1.0), ("fr", 1.0)]
    assert ex.parse_accept_language("en-US") == [("en-US", 1.0)]


def test_split_quoted_fields_handles_comma_inside_quotes(ex):
    got = ex.split_quoted_fields('"Alpha, Inc.",acct_9,1250')
    assert got == ["Alpha, Inc.", "acct_9", "1250"], (
        f"得到 {got!r}——普通 line.split(',') 会把引号里的逗号也切开，得到 4 段而不是 3 段"
    )


def test_split_quoted_fields_without_quotes_and_with_stray_spaces(ex):
    assert ex.split_quoted_fields("acct_9,1250") == ["acct_9", "1250"]
    assert ex.split_quoted_fields('"Beta Corp", acct_2 , 500') == ["Beta Corp", "acct_2", "500"]


def test_parse_charge_record_matches_worked_example_then_rejects_bad_lines(ex):
    got = ex.parse_charge_record("CHARGE, ch_1 ,acct_9, 12.50 ")
    assert got == ex.ChargeRecord(kind="CHARGE", id="ch_1", acct="acct_9", cents=1250), f"得到 {got!r}"
    # 空行 / 只有空白：没有记录可解析。
    assert ex.parse_charge_record("") is None
    assert ex.parse_charge_record("   ") is None
    # 少了一个字段：不能盲目解包（会 ValueError），要先判 len(parts) 再返回 None。
    assert ex.parse_charge_record("CHARGE,ch_1,acct_9") is None
    # 多了一个字段（比如混进了别的记录类型）：同样返回 None。
    assert ex.parse_charge_record("CHARGE,ch_1,acct_9,1250,US") is None
