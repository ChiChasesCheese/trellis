"""ex02 测试。运行：python -m pytest test_ex02.py -q"""
import io


def test_parse_events_skips_blank_and_converts(ex):
    lines = ["1,charge,100", "", "   ", "2,refund,-40", "3,charge,5"]
    got = ex.parse_events(lines)
    assert [(e.ts, e.kind, e.amount) for e in got] == [(1, "charge", 100), (2, "refund", -40), (3, "charge", 5)]
    assert isinstance(got[0], ex.Event)
    assert ex.parse_events([]) == []


def test_counter2_top_with_tiebreak(ex):
    c = ex.Counter2()
    assert c.top() is None
    for k in ["b", "a", "b", "a", "c"]:
        c.add(k)
    assert c.top() == "a"          # a 和 b 都是 2 次，字典序最小
    c.add("b")
    assert c.top() == "b"


def test_main_reads_stdin_and_writes_sorted_totals(ex):
    stdin = io.StringIO("1,charge,100\n2,refund,-40\n\n3,charge,5\n4,fee,1\n")
    stdout = io.StringIO()
    ex.main(stdin, stdout)
    assert stdout.getvalue() == "charge,105\nfee,1\nrefund,-40\n"


def test_main_empty_input_prints_nothing(ex):
    stdout = io.StringIO()
    ex.main(io.StringIO(""), stdout)
    assert stdout.getvalue() == ""
