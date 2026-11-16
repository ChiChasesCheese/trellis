import importlib
import itertools
import math
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError


def fails(status, code, fn, *args):
    """调用必须抛 ServiceError(status, code)。"""
    with pytest.raises(ServiceError) as info:
        fn(*args)
    assert (info.value.status, info.value.code) == (status, code)


def make(stream=None):
    service = impl.CurrencyExchangeService()
    if stream is not None:
        assert service.register_rates(stream)[0] == 201
    return service


def best(service, source, target):
    status, body = service.get_best_rate(source, target)
    assert status == 200
    return body


# ---- README 里的例子 ----

def test_readme_worked_example():
    service = make()
    assert service.register_rates("USD:EUR:0.9,EUR:CAD:1.5,USD:CAD:1.2") == (201, {"registered_count": 3})
    assert service.get_direct_rate("USD", "CAD") == (200, {"from": "USD", "to": "CAD", "rate": 1.2})
    status, body = service.get_single_hop_rates("USD", "CAD")
    assert status == 200 and body["rates"] == [pytest.approx(1.2), pytest.approx(1.35)]
    body = best(service, "USD", "CAD")
    assert body["path"] == ["USD", "EUR", "CAD"] and body["best_rate"] == pytest.approx(1.35)
    assert set(body) == {"from", "to", "best_rate", "path"}


def test_readme_rejected_batch_keeps_old_rate():
    service = make("GBP:JPY:180")
    fails(400, "invalid_input", service.register_rates, "GBP:JPY:200,JPY:usd:2")
    assert service.get_direct_rate("GBP", "JPY")[1]["rate"] == 180
    fails(404, "route_not_found", service.get_direct_rate, "JPY", "GBP")  # 没有反向边
    assert service.list_pairs()[1] == [{"from_currency": "GBP", "to_currency": "JPY", "rate": 180.0}]


# ---- 登记：格式 ----

@pytest.mark.parametrize("stream", [
    None, 5, 1.5, b"USD:EUR:1", ["USD:EUR:1"], "",  # 类型不对、空串
    "USD:EUR:1,", ",USD:EUR:1", "USD:EUR:1,,EUR:CAD:2",  # 空记录
    "USD:EUR", "USD:EUR:1:2", "USD::1", ":EUR:1", "USD:EUR:", "USD:EUR:1:",  # 段数与空字段
    " USD:EUR:1", "USD:EUR:1 ", "USD :EUR:1", "USD:EUR: 1", "USD:EUR:1\n", "USD:EUR:1\t",  # 不去空白
    "usd:EUR:1", "USD:eur:1", "US:EUR:1", "USDXYZ:EUR:1", "US1:EUR:1", "ÜSD:EUR:1", "USD:USD:1",  # 货币码与自报价
])
def test_invalid_streams_rejected(stream):
    service = make("AAA:BBB:2")
    fails(400, "invalid_input", service.register_rates, stream)
    assert service.list_pairs()[1] == [{"from_currency": "AAA", "to_currency": "BBB", "rate": 2.0}]


@pytest.mark.parametrize("code", ["ABC", "ABCD", "ABCDE"])
def test_code_length_boundaries_accepted(code):
    assert make().register_rates(f"{code}:ZZZ:1")[0] == 201


@pytest.mark.parametrize("token,value", [
    ("1", 1.0), ("1.", 1.0), (".5", 0.5), ("+2.5e-1", 0.25), ("0.9", 0.9), ("1E2", 100.0),
    ("007", 7.0), ("+3", 3.0), ("1e0", 1.0), (".5E+1", 5.0),
])
def test_rate_grammar_accepts(token, value):
    service = make(f"AAA:BBB:{token}")
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == value


@pytest.mark.parametrize("token", [
    "", "e5", "1e", "1e+", ".", "+", "-", "1.2.3", "1_0", "0x10", "nan", "NaN", "inf", "Infinity", "-inf",
    "١٢", "1٫5", "１", "1 ", " 1", "1,5", "--1", "1e1.5", "-1", "-0", "0", "0.0", ".0e5", "+.e1",
])
def test_rate_grammar_rejects(token):
    fails(400, "invalid_input", make().register_rates, f"AAA:BBB:{token}")


def test_rate_bounds_are_inclusive_and_checked_on_parsed_value():
    service = make("AAA:BBB:1e-12,BBB:CCC:1e12,CCC:DDD:0.000000000001")
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == 1e-12
    assert service.get_direct_rate("BBB", "CCC")[1]["rate"] == 1e12
    assert service.get_direct_rate("CCC", "DDD")[1]["rate"] == 1e-12
    # 字面量比 1e12 大，但最近的 binary64 恰好就是 1e12：合法
    assert float("1000000000000.00000001") == 1e12
    assert make("EEE:FFF:1000000000000.00000001").get_direct_rate("EEE", "FFF")[1]["rate"] == 1e12
    # 解析后的值越界：非法
    for token in ["1e-13", "9.99e-13", "1.0000000000001e12", "1e13", "1e999", "1e-999", "1e99999999999999"]:
        fails(400, "invalid_input", make().register_rates, f"AAA:BBB:{token}")


def test_very_long_digit_strings_parse_without_error():
    digits = "1" + "0" * 5000
    fails(400, "invalid_input", make().register_rates, f"AAA:BBB:{digits}")  # 数值太大
    service = make(f"AAA:BBB:0.{'0' * 5000}1e5001")  # 小数点后 5001 位的 1，乘 1e5001：值是 1
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == 1.0


# ---- 登记：重复、计数、方向、货币数 ----

def test_duplicates_last_wins_and_count_includes_duplicates():
    service = make()
    assert service.register_rates("AAA:BBB:2,AAA:BBB:3,AAA:BBB:4") == (201, {"registered_count": 3})
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == 4
    assert service.register_rates("AAA:BBB:5") == (201, {"registered_count": 1})
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == 5
    assert len(service.list_pairs()[1]) == 1


def test_registration_is_directed():
    service = make("AAA:BBB:2")
    fails(404, "route_not_found", service.get_direct_rate, "BBB", "AAA")
    fails(404, "route_not_found", service.get_single_hop_rates, "BBB", "AAA")
    fails(404, "route_not_found", service.get_best_rate, "BBB", "AAA")


def test_eight_currencies_allowed_ninth_rejected_across_calls():
    names = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]
    chain = ",".join(f"{a}:{b}:2" for a, b in zip(names, names[1:]))  # 8 种，7 条边
    service = make(chain)
    assert len(service.list_pairs()[1]) == 7
    assert service.register_rates("HHH:AAA:3,AAA:HHH:4")[0] == 201  # 已有货币之间随便加边
    fails(400, "invalid_input", service.register_rates, "AAA:III:2")  # 第 9 种
    fails(404, "currency_not_found", service.get_direct_rate, "AAA", "III")


def test_ninth_currency_inside_one_batch_rejected():
    nine = "AAA:BBB:2,CCC:DDD:2,EEE:FFF:2,GGG:HHH:2,HHH:III:2"
    fails(400, "invalid_input", make().register_rates, nine)
    eight = "AAA:BBB:2,CCC:DDD:2,EEE:FFF:2,GGG:HHH:2"
    assert make().register_rates(eight)[0] == 201


def test_target_only_currency_counts_toward_the_limit():
    service = make("AAA:BBB:2,AAA:CCC:2,AAA:DDD:2,AAA:EEE:2,AAA:FFF:2,AAA:GGG:2,AAA:HHH:2")
    fails(400, "invalid_input", service.register_rates, "AAA:III:2")


# ---- 原子登记 ----

def test_rejected_batch_changes_nothing_not_even_new_currencies_or_overwrites():
    service = make("AAA:BBB:2,BBB:CCC:3")
    before = service.list_pairs()
    fails(400, "invalid_input", service.register_rates, "AAA:BBB:9,DDD:EEE:5,EEE:FFF:oops")
    assert service.list_pairs() == before
    fails(404, "currency_not_found", service.get_direct_rate, "DDD", "EEE")  # 同批里的新货币没有漏进去
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == 2  # 同批里更早的覆盖也没有生效


def test_batch_exceeding_currency_limit_leaves_earlier_records_unpublished():
    service = make("AAA:BBB:2")
    batch = "AAA:BBB:7,CCC:DDD:2,EEE:FFF:2,GGG:HHH:2,III:JJJ:2"  # 前几条都合法，整批超限
    fails(400, "invalid_input", service.register_rates, batch)
    assert service.list_pairs()[1] == [{"from_currency": "AAA", "to_currency": "BBB", "rate": 2.0}]


def test_failed_calls_leave_queries_working():
    service = make("AAA:BBB:2")
    for bad in ["AAA:BBB:x", None, "", "AAA:AAA:2"]:
        fails(400, "invalid_input", service.register_rates, bad)
    assert service.get_direct_rate("AAA", "BBB")[1]["rate"] == 2


# ---- 查询：错误优先级 ----

def test_error_precedence_format_then_known_then_route():
    service = make("AAA:BBB:2,CCC:DDD:2")
    fails(400, "invalid_input", service.get_direct_rate, "aaa", "ZZZ")  # 格式错先于未知
    fails(400, "invalid_input", service.get_direct_rate, "ZZZ", "aaa")
    fails(400, "invalid_input", service.get_best_rate, None, "AAA")
    fails(400, "invalid_input", service.get_single_hop_rates, "AAA", 5)
    fails(400, "invalid_input", service.get_direct_rate, "AA", "BBB")
    fails(404, "currency_not_found", service.get_direct_rate, "AAA", "ZZZ")
    fails(404, "currency_not_found", service.get_direct_rate, "ZZZ", "AAA")
    fails(404, "currency_not_found", service.get_best_rate, "ZZZ", "YYY")
    fails(404, "route_not_found", service.get_direct_rate, "AAA", "CCC")  # 都认识，但没有路
    fails(404, "route_not_found", service.get_single_hop_rates, "AAA", "CCC")
    fails(404, "route_not_found", service.get_best_rate, "AAA", "CCC")


def test_queries_on_an_empty_service():
    service = make()
    fails(404, "currency_not_found", service.get_direct_rate, "AAA", "BBB")
    fails(404, "currency_not_found", service.get_best_rate, "AAA", "AAA")
    fails(400, "invalid_input", service.get_best_rate, "AAA", "bbb")


def test_same_known_code_results():
    service = make("AAA:BBB:2")
    for code in ("AAA", "BBB"):  # BBB 只作过终点，也算出现过
        assert service.get_direct_rate(code, code) == (200, {"from": code, "to": code, "rate": 1})
        assert service.get_single_hop_rates(code, code) == (200, {"from": code, "to": code, "rates": [1]})
        assert service.get_best_rate(code, code) == (200, {"from": code, "to": code, "best_rate": 1, "path": [code]})
    fails(404, "currency_not_found", service.get_direct_rate, "ZZZ", "ZZZ")


# ---- 单次中转 ----

def test_single_hop_includes_direct_and_every_distinct_middle_sorted_with_duplicates():
    service = make("SSS:TTT:6,SSS:MMM:2,MMM:TTT:3,SSS:NNN:3,NNN:TTT:2,SSS:OOO:1,OOO:TTT:5")
    rates = service.get_single_hop_rates("SSS", "TTT")[1]["rates"]
    assert rates == [5.0, 6.0, 6.0, 6.0]  # 5 = 1*5；三条路径都是 6，重复保留，直达 6 也在里面
    assert rates == sorted(rates)


def test_single_hop_excludes_longer_routes_and_endpoints_as_middle():
    service = make("AAA:BBB:2,BBB:CCC:3,CCC:DDD:4,DDD:AAA:5,BBB:AAA:7")
    assert service.get_single_hop_rates("AAA", "CCC")[1]["rates"] == [6.0]
    fails(404, "route_not_found", service.get_single_hop_rates, "AAA", "DDD")  # 要三条边，不算
    assert service.get_single_hop_rates("AAA", "BBB")[1]["rates"] == [2.0]  # 经 BBB 或 AAA 自己中转的不算


def test_single_hop_without_direct_edge():
    service = make("AAA:BBB:2,BBB:CCC:5")
    assert service.get_single_hop_rates("AAA", "CCC")[1]["rates"] == [10.0]


# ---- 最优路线 ----

def test_best_never_walks_a_profitable_cycle():
    service = make("AAA:BBB:2,BBB:AAA:2,BBB:CCC:1")  # AAA-BBB-AAA 每圈翻 4 倍
    body = best(service, "AAA", "CCC")
    assert body["path"] == ["AAA", "BBB", "CCC"] and body["best_rate"] == 2


def test_best_stops_at_target_and_does_not_pass_through_it():
    service = make("AAA:BBB:1,BBB:CCC:10,CCC:BBB:10")
    assert best(service, "AAA", "BBB")["path"] == ["AAA", "BBB"]


def test_best_prefers_the_larger_product_even_with_more_hops():
    service = make("AAA:DDD:1,AAA:BBB:2,BBB:CCC:2,CCC:DDD:2")
    body = best(service, "AAA", "DDD")
    assert body["path"] == ["AAA", "BBB", "CCC", "DDD"] and body["best_rate"] == 8


def test_best_within_tolerance_prefers_fewer_hops_and_returns_its_own_product():
    # 两跳 2.0，一跳 2.0 - 0.9e-5：差在容差内，选一跳，返回它自己的乘积
    low = 2.0 - 0.9e-5
    service = make(f"AAA:BBB:1,BBB:CCC:2,AAA:CCC:{low!r}")
    body = best(service, "AAA", "CCC")
    assert body["path"] == ["AAA", "CCC"] and body["best_rate"] == low
    assert body["best_rate"] < 2.0


def test_best_outside_tolerance_keeps_the_maximum():
    service = make(f"AAA:BBB:1,BBB:CCC:2,AAA:CCC:{2.0 - 1.5e-5!r}")
    assert best(service, "AAA", "CCC")["path"] == ["AAA", "BBB", "CCC"]


def test_difference_of_exactly_the_tolerance_is_still_eligible():
    assert 2e-5 - 1e-5 == 1e-5  # 浮点里恰好等于容差，不多不少
    service = make("AAA:MMM:2e-5,MMM:TTT:1,AAA:TTT:1e-5")
    body = best(service, "AAA", "TTT")
    assert body["path"] == ["AAA", "TTT"] and body["best_rate"] == 1e-5


def test_tolerance_is_anchored_to_the_global_maximum_not_the_chosen_path():
    # 三条路径：三条边 M；两条边 M - 0.9e-5；一条边 M - 1.8e-5。一条边相对两条边在容差内，相对 M 不在。
    m = 2.0
    service = make(
        "AAA:BBB:1,BBB:CCC:1,CCC:TTT:2,"  # 三条边，乘积 M
        f"AAA:DDD:1,DDD:TTT:{m - 0.9e-5!r},"  # 两条边，M - 0.9e-5
        f"AAA:TTT:{m - 1.8e-5!r}"  # 一条边，M - 1.8e-5
    )
    body = best(service, "AAA", "TTT")
    assert body["path"] == ["AAA", "DDD", "TTT"] and body["best_rate"] == m - 0.9e-5


def test_tolerance_tie_on_hops_breaks_by_lexicographic_code_sequence():
    service = make("AAA:ZZZ:1,AAA:MMM:1,AAA:BBB:1,ZZZ:TTT:2,MMM:TTT:2,BBB:TTT:2")
    assert best(service, "AAA", "TTT")["path"] == ["AAA", "BBB", "TTT"]


def test_lexicographic_comparison_is_by_code_not_by_joined_string():
    # 按代码序列比较："ABC" < "ABCD"；拼成字符串后 "ABCDTTT..." 也一样，换一组能区分两种比法
    service = make("SRC:ABC:1,SRC:ABCD:1,ABC:TTT:2,ABCD:TTT:2")
    assert best(service, "SRC", "TTT")["path"] == ["SRC", "ABC", "TTT"]


def test_product_is_multiplied_left_to_right_starting_from_one():
    rates = [0.1, 0.7, 1.3, 3.1]
    service = make("AAA:BBB:0.1,BBB:CCC:0.7,CCC:DDD:1.3,DDD:EEE:3.1")
    expected = 1.0
    for rate in rates:
        expected *= rate
    assert best(service, "AAA", "EEE")["best_rate"] == expected


def test_best_with_seven_edges_at_the_bounds_stays_finite_and_nonzero():
    names = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]
    big = ",".join(f"{a}:{b}:1e12" for a, b in zip(names, names[1:]))
    small = ",".join(f"{a}:{b}:1e-12" for a, b in zip(names, names[1:]))
    top = best(make(big), "AAA", "HHH")["best_rate"]
    bottom = best(make(small), "AAA", "HHH")["best_rate"]
    assert math.isfinite(top) and top == pytest.approx(1e84)
    assert bottom > 0 and bottom == pytest.approx(1e-84)


def test_eight_currency_complete_graph_is_fast_enough_and_matches_oracle():
    names = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]
    rng = random.Random(7)
    quotes = {(a, b): round(rng.uniform(0.5, 2.0), 3) for a in names for b in names if a != b}
    service = make(",".join(f"{a}:{b}:{r}" for (a, b), r in quotes.items()))
    assert best(service, "AAA", "HHH")["best_rate"] == pytest.approx(oracle_best(quotes, "AAA", "HHH")[1])


def oracle_best(quotes, source, target):
    """另一种写法：对所有中间货币子集的所有排列穷举，再按规则选。"""
    others = sorted({c for pair in quotes for c in pair} - {source, target})
    found = []
    for size in range(len(others) + 1):
        for middle in itertools.permutations(others, size):
            path = [source, *middle, target]
            product = 1.0
            for a, b in zip(path, path[1:]):
                if (a, b) not in quotes:
                    break
                product *= quotes[(a, b)]
            else:
                found.append((path, product))
    if not found:
        return None
    top = max(p for _, p in found)
    eligible = [(path, p) for path, p in found if top - p <= 1e-5]
    return min(eligible, key=lambda item: (len(item[0]), item[0]))


@pytest.mark.parametrize("seed", range(12))
def test_best_and_single_hop_match_the_oracle_on_random_graphs(seed):
    rng = random.Random(seed)
    names = rng.sample(["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"], rng.randint(4, 8))
    quotes = {}
    for a in names:
        for b in names:
            if a != b and rng.random() < 0.45:
                quotes[(a, b)] = rng.choice([0.5, 1.0, 1.5, 2.0, 0.25, 4.0, 1.000004, 0.999996])
    if not quotes:
        return
    service = make(",".join(f"{a}:{b}:{r}" for (a, b), r in quotes.items()))
    for source in names:
        for target in names:
            known = {c for pair in quotes for c in pair}
            if source not in known or target not in known or source == target:
                continue
            expected = oracle_best(quotes, source, target)
            if expected is None:
                fails(404, "route_not_found", service.get_best_rate, source, target)
            else:
                body = best(service, source, target)
                assert (body["path"], body["best_rate"]) == (expected[0], expected[1])
            hops = sorted(
                ([quotes[(source, target)]] if (source, target) in quotes else [])
                + [quotes[(source, m)] * quotes[(m, target)] for m in names
                   if m not in (source, target) and (source, m) in quotes and (m, target) in quotes]
            )
            if hops:
                assert service.get_single_hop_rates(source, target)[1]["rates"] == hops
            else:
                fails(404, "route_not_found", service.get_single_hop_rates, source, target)


# ---- 列表 ----

def test_list_pairs_sorted_by_source_then_target_with_exact_fields():
    service = make("CCC:AAA:3,AAA:CCC:1,AAA:BBB:2,BBB:AAA:4")
    status, rows = service.list_pairs()
    assert status == 200
    assert [(r["from_currency"], r["to_currency"]) for r in rows] == [
        ("AAA", "BBB"), ("AAA", "CCC"), ("BBB", "AAA"), ("CCC", "AAA")]
    assert all(set(r) == {"from_currency", "to_currency", "rate"} for r in rows)
    assert service.list_pairs("AAA")[1] == rows[:2]
    assert service.list_pairs(None)[1] == rows


def test_list_pairs_filter_rules():
    service = make("AAA:BBB:2")
    assert service.list_pairs("BBB") == (200, [])  # 只作终点：已知，没有出边
    fails(404, "currency_not_found", service.list_pairs, "ZZZ")
    for bad in ["aaa", "", "AA", 5, "AAAAAA", "AAA "]:
        fails(400, "invalid_input", service.list_pairs, bad)
    assert make().list_pairs() == (200, [])
    fails(404, "currency_not_found", make().list_pairs, "AAA")


# ---- 快照与隔离 ----

def mutate(value):
    if isinstance(value, dict):
        for key in list(value):
            mutate(value[key])
        value.clear()
    elif isinstance(value, list):
        for item in value:
            mutate(item)
        value.clear()


def test_returned_results_are_detached_snapshots():
    service = make("AAA:BBB:2,BBB:CCC:3,AAA:CCC:5")
    calls = [
        lambda: service.get_direct_rate("AAA", "CCC"),
        lambda: service.get_single_hop_rates("AAA", "CCC"),
        lambda: service.get_best_rate("AAA", "CCC"),
        lambda: service.list_pairs(),
        lambda: service.list_pairs("AAA"),
    ]
    expected = [call() for call in calls]
    for call in calls:
        _, body = call()
        mutate(body)
    assert [call() for call in calls] == expected  # 返回值被清空之后，再问一次，答案不变
    assert service.list_pairs()[1][0]["rate"] == 2.0  # 清空返回值之后，服务的数据还在


def test_a_held_result_does_not_change_when_more_rates_are_registered():
    service = make("AAA:BBB:2,BBB:CCC:3")
    _, held = service.get_best_rate("AAA", "CCC")
    _, rows = service.list_pairs()
    snapshot = (dict(held, path=list(held["path"])), [dict(r) for r in rows])
    service.register_rates("AAA:CCC:100,AAA:BBB:9")
    assert held == snapshot[0] and rows == snapshot[1]
    assert held["path"] == ["AAA", "BBB", "CCC"]


def test_instances_share_no_state():
    first, second = make("AAA:BBB:2"), make("CCC:DDD:3")
    fails(404, "currency_not_found", second.get_direct_rate, "AAA", "BBB")
    fails(404, "currency_not_found", first.get_direct_rate, "CCC", "DDD")
    assert make().list_pairs() == (200, [])


def test_returned_numbers_are_real_numbers_not_bools():
    service = make("AAA:BBB:1")
    for _, body in [service.get_direct_rate("AAA", "BBB"), service.get_direct_rate("AAA", "AAA")]:
        assert type(body["rate"]) in (int, float)
    _, body = service.get_best_rate("AAA", "AAA")
    assert type(body["best_rate"]) in (int, float) and body["path"] == ["AAA"]
    assert all(type(r) in (int, float) for r in service.get_single_hop_rates("AAA", "AAA")[1]["rates"])
