import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError

CAP = 2_147_483_647

KETTLE = ["NL,kettle,incremental,1,4,300", "NL,kettle,fixed,5,9,900", "NL,kettle,incremental,10,*,150"]
LAMP = ["NL,lamp,incremental,1,*,250"]


def fails(status, code, fn, *args):
    """调用必须抛 ServiceError(status, code)。"""
    with pytest.raises(ServiceError) as info:
        fn(*args)
    assert (info.value.status, info.value.code) == (status, code)


def make(*batches):
    service = impl.ShippingService()
    for rules in batches:
        assert service.register_rules(list(rules))[0] == 201
    return service


def quote(service, country, items):
    status, body = service.calculate_shipping(country, items)
    assert status == 200
    return body


# ---- 合同里的例子 ----

def test_worked_example_mixed_tiers_and_merged_lines():
    service = make(KETTLE + LAMP)
    # kettle 合并后 11 件：4*300 + 900 + 2*150 = 2400；lamp 10 件：2500
    body = quote(service, "NL", ["lamp,10", "kettle,6", "kettle,5"])
    assert body == {"total_cost": 4900, "country": "NL",
                    "breakdown": [{"product": "kettle", "quantity": 11, "cost": 2400},
                                  {"product": "lamp", "quantity": 10, "cost": 2500}]}


def test_registered_count_is_the_number_of_input_lines():
    service = impl.ShippingService()
    assert service.register_rules(KETTLE + LAMP) == (201, {"registered_count": 4})
    assert service.register_rules(["BR,poster,fixed,1,*,700"]) == (201, {"registered_count": 1})


# ---- 登记：语法（400） ----

BAD_SYNTAX = [
    "NL,lamp,incremental,1,*",  # 五段
    "NL,lamp,incremental,1,*,250,9",  # 七段
    "", ",,,,,", "NL,lamp,incremental,1,*,",  # 空行、空字段
    "nl,lamp,incremental,1,*,250", "N,lamp,incremental,1,*,250", "NLNLNL,lamp,incremental,1,*,250",  # 国家
    "N1,lamp,incremental,1,*,250", "NL ,lamp,incremental,1,*,250", " NL,lamp,incremental,1,*,250",
    "NL,,incremental,1,*,250", "NL,la mp,incremental,1,*,250", "NL,lamp!,incremental,1,*,250",  # 商品
    "NL," + "a" * 33 + ",incremental,1,*,250", "NL,lampé,incremental,1,*,250",
    "NL,lamp,Incremental,1,*,250", "NL,lamp,flat,1,*,250", "NL,lamp,,1,*,250", "NL,lamp,fixed ,1,*,250",  # 类型
    "NL,lamp,fixed,-1,*,250", "NL,lamp,fixed,+1,*,250", "NL,lamp,fixed,1.0,*,250", "NL,lamp,fixed,1e1,*,250",  # 数字写法
    "NL,lamp,fixed,0x1,*,250", "NL,lamp,fixed,1_0,*,250", "NL,lamp,fixed, 1,*,250", "NL,lamp,fixed,١,*,250",
    "NL,lamp,fixed,1,**,250", "NL,lamp,fixed,1,-,250", "NL,lamp,fixed,1,∞,250", "NL,lamp,fixed,1,-3,250",  # 最大数量
    "NL,lamp,fixed,1,*,0", "NL,lamp,fixed,1,*,-5", "NL,lamp,fixed,1,*,000",  # 费用必须为正
    "NL,lamp,fixed,1000001,*,250", "NL,lamp,fixed,1,1000001,250", "NL,lamp,fixed,1,*,1000001",  # 超过 1,000,000
    "NL,lamp,fixed,1,*,250\n", "NL,lamp,fixed,1,*,250\t",  # 末尾空白
]


@pytest.mark.parametrize("line", BAD_SYNTAX)
def test_bad_line_syntax_is_400(line):
    service = make(LAMP)
    fails(400, "invalid_input", service.register_rules, [line])
    assert service.list_rules()[1] == [{"country": "NL", "product": "lamp", "type": "incremental",
                                        "min_quantity": 1, "max_quantity": None, "cost_cents": 250}]


@pytest.mark.parametrize("batch", [[], (), None, "NL,lamp,fixed,1,*,250", {"a": 1}, 7, [None], [5],
                                   [b"NL,lamp,fixed,1,*,250"], [["NL", "lamp", "fixed", 1, "*", 250]]])
def test_bad_batch_container_is_400(batch):
    fails(400, "invalid_input", impl.ShippingService().register_rules, batch)


def test_token_bounds_are_inclusive_and_leading_zeros_are_fine():
    service = make(["JP,pen,fixed,0001,0999999,0000001000000", "JP,pen,incremental,1000000,*,1"])
    rows = service.list_rules()[1]
    assert [(r["min_quantity"], r["max_quantity"], r["cost_cents"]) for r in rows] == [
        (1, 999999, 1_000_000), (1_000_000, None, 1)]
    long_zeros = "0" * 5000
    service.register_rules([f"JP,ink,fixed,{long_zeros}1,*,{long_zeros}7"])  # 超长的零串不能让 int() 抛错
    assert quote(service, "JP", [f"ink,{long_zeros}3"])["total_cost"] == 7


def test_syntax_error_anywhere_beats_a_schedule_error():
    service = make(LAMP)
    batch = ["JP,pen,fixed,2,*,100", "JP,cup,fixed,1,*,100", "JP,cup,fixed,1,*,100", "JP,cup,fixed,x,*,100"]
    fails(400, "invalid_input", service.register_rules, batch)
    fails(422, "invalid_rules", service.register_rules, batch[:3])


# ---- 登记：分段（422） ----

BAD_SCHEDULES = {
    "从 2 开始": ["fixed,2,*,5"],
    "从 0 开始（零锚点）": ["fixed,0,*,5"],
    "零锚点后接 1": ["fixed,0,0,5", "fixed,1,*,5"],
    "有缺口": ["fixed,1,2,5", "fixed,4,*,5"],
    "重叠": ["fixed,1,5,5", "fixed,5,*,5"],
    "起点重复": ["fixed,1,3,5", "fixed,1,*,5"],
    "完全相同的两行": ["fixed,1,*,5", "fixed,1,*,5"],
    "无上界之后还有段": ["fixed,1,*,5", "fixed,9,*,5"],
    "最大小于最小": ["fixed,1,2,5", "fixed,3,2,5", "fixed,3,*,5"],
    "末段有限": ["fixed,1,5,5"],
    "单段有限": ["incremental,1,1000000,5"],
}


@pytest.mark.parametrize("label", BAD_SCHEDULES)
def test_bad_schedule_is_422_and_changes_nothing(label):
    service = make(LAMP)
    before = service.list_rules()
    batch = ["BR,poster,fixed,1,*,10"] + ["BR,vase," + row for row in BAD_SCHEDULES[label]]
    fails(422, "invalid_rules", service.register_rules, batch)
    assert service.list_rules() == before  # 同批里合法的 poster 也没有生效
    fails(404, "country_not_found", service.calculate_shipping, "BR", ["poster,1"])


def test_valid_schedule_shapes():
    service = make([
        "AU,mug,incremental,4,*,50", "AU,mug,fixed,2,3,70", "AU,mug,incremental,1,1,10",  # 输入乱序
        "AU,bowl,fixed,1,*,500",  # 无上界的固定段
        "AU,fork,incremental,1,1,3", "AU,fork,fixed,2,2,4", "AU,fork,incremental,3,3,5", "AU,fork,fixed,4,*,6",  # 单点段
    ])
    rows = service.list_rules("AU")[1]
    assert [(r["product"], r["min_quantity"]) for r in rows] == [
        ("bowl", 1), ("fork", 1), ("fork", 2), ("fork", 3), ("fork", 4), ("mug", 1), ("mug", 2), ("mug", 4)]
    assert quote(service, "AU", ["bowl,1000000"])["total_cost"] == 500
    assert quote(service, "AU", ["fork,9"])["total_cost"] == 3 + 4 + 5 + 6


# ---- 登记：原子与替换 ----

def test_rejected_batch_leaves_old_schedules_and_other_countries_alone():
    service = make(KETTLE, ["BR,poster,fixed,1,*,10"])
    before = service.list_rules()
    fails(422, "invalid_rules", service.register_rules,
          ["NL,kettle,fixed,1,*,1", "DE,lamp,fixed,1,*,1", "DE,lamp,fixed,3,*,1"])
    assert service.list_rules() == before
    assert quote(service, "NL", ["kettle,6"])["total_cost"] == 4 * 300 + 900
    fails(404, "country_not_found", service.calculate_shipping, "DE", [])


def test_a_batch_replaces_only_the_pairs_it_touches():
    service = make(KETTLE + LAMP, ["BR,poster,fixed,1,*,10"])
    service.register_rules(["NL,kettle,fixed,1,*,111"])
    assert service.list_rules("NL")[1] == [
        {"country": "NL", "product": "kettle", "type": "fixed", "min_quantity": 1, "max_quantity": None, "cost_cents": 111},
        {"country": "NL", "product": "lamp", "type": "incremental", "min_quantity": 1, "max_quantity": None, "cost_cents": 250},
    ]
    assert quote(service, "NL", ["kettle,99"])["total_cost"] == 111
    assert quote(service, "BR", ["poster,2"])["total_cost"] == 10


def test_lines_of_one_pair_split_across_the_batch_are_collected_together():
    service = impl.ShippingService()
    service.register_rules(["NL,kettle,fixed,5,*,900", "NL,lamp,fixed,1,*,1", "NL,kettle,incremental,1,4,300"])
    assert quote(service, "NL", ["kettle,5"])["total_cost"] == 4 * 300 + 900
    fails(422, "invalid_rules", service.register_rules, ["NL,kettle,fixed,5,*,900"])  # 只剩一段，不从 1 起


# ---- 报价：错误优先级 ----

def test_error_precedence_runs_in_the_documented_order():
    service = make(KETTLE, ["NL,gem,incremental,1,*,1000000"])
    bad_item, too_dear = "kettle,x", "gem,2148"  # 2148 * 1,000,000 超过上界
    # ① 国家语法或容器不对：先于一切
    fails(400, "invalid_input", service.calculate_shipping, "nl", ["nope,1"])
    fails(400, "invalid_input", service.calculate_shipping, "NL", "kettle,1")
    fails(400, "invalid_input", service.calculate_shipping, "NL", None)
    fails(400, "invalid_input", service.calculate_shipping, None, [])
    # ② 合法国家但没有费率：404，哪怕订单畸形或为空
    fails(404, "country_not_found", service.calculate_shipping, "DE", [bad_item])
    fails(404, "country_not_found", service.calculate_shipping, "DE", [])
    # ③ 任何一行畸形：先于商品缺失，和位置无关
    fails(400, "invalid_input", service.calculate_shipping, "NL", ["ghost,1", bad_item])
    fails(400, "invalid_input", service.calculate_shipping, "NL", [bad_item, "ghost,1"])
    # ④ 商品缺失：先于金额超限
    fails(404, "product_not_found", service.calculate_shipping, "NL", [too_dear, "ghost,1"])
    # ⑤ 金额超限
    fails(400, "invalid_input", service.calculate_shipping, "NL", [too_dear, "kettle,1"])


@pytest.mark.parametrize("item", [
    "kettle", "kettle,1,2", "", ",3", "kettle,", "kettle,0", "kettle,-1", "kettle,+1", "kettle,1.5", "kettle,1e2",
    "kettle, 1", "kettle,1 ", "kettle,١", "kettle,1000001", "ket tle,1", "Kettle,1,", 5, None, ["kettle", 1]])
def test_malformed_item_is_400(item):
    fails(400, "invalid_input", make(KETTLE).calculate_shipping, "NL", [item])


def test_unknown_product_is_exact_and_case_sensitive():
    service = make(KETTLE)
    fails(404, "product_not_found", service.calculate_shipping, "NL", ["Kettle,1"])
    fails(404, "product_not_found", service.calculate_shipping, "NL", ["kettle,1", "lamp,1"])


def test_aggregate_quantity_is_bounded_even_when_every_line_is_fine():
    service = make(KETTLE)
    fails(400, "invalid_input", service.calculate_shipping, "NL", ["kettle,600000", "kettle,400001"])
    assert quote(service, "NL", ["kettle,600000", "kettle,400000"])["breakdown"][0]["quantity"] == 1_000_000
    # 不同商品各自一份额度：超限只看每个商品自己的合计
    both = make(KETTLE + LAMP)
    assert quote(both, "NL", ["kettle,1000000", "lamp,1000000"])["total_cost"] == 4 * 300 + 900 + 999991 * 150 + 250_000_000


def test_empty_order_in_a_known_country():
    service = make(KETTLE)
    assert service.calculate_shipping("NL", []) == (200, {"total_cost": 0, "country": "NL", "breakdown": []})


# ---- 报价：算价 ----

def test_repeated_lines_are_merged_before_a_fixed_tier_is_priced():
    service = make(["DE,jar,fixed,1,*,400"])
    together = quote(service, "DE", ["jar,2"])["total_cost"]
    split = quote(service, "DE", ["jar,1", "jar,1"])
    assert together == 400
    assert split["total_cost"] == 400 and split["breakdown"] == [{"product": "jar", "quantity": 2, "cost": 400}]


def test_every_entered_tier_adds_its_fee_and_the_next_never_replaces_the_previous():
    service = make(["DE,jar,incremental,1,2,10", "DE,jar,fixed,3,5,100", "DE,jar,fixed,6,6,1000", "DE,jar,incremental,7,*,1"])
    expected = {1: 10, 2: 20, 3: 120, 5: 120, 6: 1120, 7: 1121, 10: 1124}
    for count, cost in expected.items():
        assert quote(service, "DE", [f"jar,{count}"])["total_cost"] == cost


def test_breakdown_is_sorted_by_ascii_product_name():
    names = ["b", "a", "Z", "_x", "-y", "9", "A1", "aa"]
    service = make([f"DE,{name},fixed,1,*,1" for name in names])
    rows = quote(service, "DE", [f"{name},1" for name in names])["breakdown"]
    assert [row["product"] for row in rows] == sorted(names) == ["-y", "9", "A1", "Z", "_x", "a", "aa", "b"]


def test_cost_bound_is_checked_per_product_and_for_the_total():
    service = make(["DE,gem,incremental,1,*,1000000", "DE,pearl,incremental,1,*,1000000"])
    assert quote(service, "DE", ["gem,2147"])["total_cost"] == 2_147_000_000  # 上界以内
    fails(400, "invalid_input", service.calculate_shipping, "DE", ["gem,2148"])  # 2,148,000,000 超过
    fails(400, "invalid_input", service.calculate_shipping, "DE", ["gem,1000000"])  # 10^12，32 位或浮点实现都会出错
    assert quote(service, "DE", ["gem,1500", "gem,600"])["total_cost"] == 2_100_000_000  # 合并后 2100 件，仍在上界内
    # 每个商品都不超限，合起来超限
    fails(400, "invalid_input", service.calculate_shipping, "DE", ["gem,1500", "pearl,1500"])


def test_one_product_fee_exactly_at_the_cap_is_allowed():
    # 2147 个单件固定段各收 1,000,000，末段再收 483,647：买 2148 件恰好是 2,147,483,647
    singles = [f"DE,gem,fixed,{k},{k},1000000" for k in range(1, 2148)]
    service = make(singles + ["DE,gem,fixed,2148,*,483647"])
    assert quote(service, "DE", ["gem,2148"])["total_cost"] == CAP
    assert quote(service, "DE", ["gem,2147"])["total_cost"] == 2_147_000_000
    service.register_rules(singles + ["DE,gem,fixed,2148,*,483648"])
    fails(400, "invalid_input", service.calculate_shipping, "DE", ["gem,2148"])


def test_total_exactly_at_the_cap_is_allowed_and_one_cent_more_is_not():
    # 2147 个商品各收 1,000,000，再加 483,647，合计恰好 2,147,483,647
    names = [f"p{i}" for i in range(2147)]
    service = make([f"DE,{n},fixed,1,*,1000000" for n in names] + ["DE,tail,fixed,1,*,483647"])
    items = [f"{n},1" for n in names] + ["tail,1"]
    assert quote(service, "DE", items)["total_cost"] == CAP
    service.register_rules(["DE,tail,fixed,1,*,483648"])
    fails(400, "invalid_input", service.calculate_shipping, "DE", items)


# ---- 列表 ----

def test_list_is_sorted_by_country_product_then_minimum_quantity():
    service = make(["NL,b,fixed,2,*,1", "NL,b,fixed,1,1,1", "BR,z,fixed,1,*,1", "NL,B,fixed,1,*,1", "AU,a,fixed,1,*,1"])
    keys = [(r["country"], r["product"], r["min_quantity"]) for r in service.list_rules()[1]]
    assert keys == [("AU", "a", 1), ("BR", "z", 1), ("NL", "B", 1), ("NL", "b", 1), ("NL", "b", 2)]


def test_list_row_shape_and_filters():
    service = make(KETTLE + ["BR,poster,fixed,1,*,10"])
    status, rows = service.list_rules("NL")
    assert status == 200 and rows[0] == {"country": "NL", "product": "kettle", "type": "incremental",
                                         "min_quantity": 1, "max_quantity": 4, "cost_cents": 300}
    assert rows[-1]["max_quantity"] is None and len(rows) == 3
    assert len(service.list_rules(None)[1]) == 4
    for nothing in ("DE", "", "nl", "NL ", "N", "NLX", "!!"):  # 没有匹配：空列表，不是错误
        assert service.list_rules(nothing) == (200, [])
    fails(404, "country_not_found", service.calculate_shipping, "DE", [])  # 过滤没有创造出国家
    assert impl.ShippingService().list_rules() == (200, [])


# ---- 独立状态与快照 ----

def test_returned_values_and_inputs_are_detached_from_internal_state():
    rules = list(KETTLE)
    service = impl.ShippingService()
    service.register_rules(rules)
    rules.clear()  # 调用方清空自己的列表，不影响已登记的费率
    assert len(service.list_rules()[1]) == 3
    items = ["kettle,6", "kettle,1"]
    body = quote(service, "NL", items)
    assert items == ["kettle,6", "kettle,1"]  # 订单输入没被改
    assert body["total_cost"] == 4 * 300 + 900 and body["breakdown"][0]["quantity"] == 7

    held_rows = service.list_rules()[1]
    snapshot = [dict(row) for row in held_rows]
    held_body = quote(service, "NL", ["kettle,3"])
    held_copy = {"total_cost": held_body["total_cost"], "breakdown": [dict(r) for r in held_body["breakdown"]]}
    held_rows[0]["cost_cents"] = -1
    held_rows.clear()
    held_body["breakdown"].clear()
    held_body["total_cost"] = -1
    assert service.list_rules()[1] == snapshot
    assert quote(service, "NL", ["kettle,3"]) == {"total_cost": held_copy["total_cost"], "country": "NL",
                                                  "breakdown": held_copy["breakdown"]}


def test_results_taken_before_a_registration_do_not_change_afterwards():
    service = make(KETTLE)
    before_rows = service.list_rules()[1]
    before_copy = [dict(row) for row in before_rows]
    before_quote = quote(service, "NL", ["kettle,6"])
    service.register_rules(["NL,kettle,fixed,1,*,5", "NL,lamp,fixed,1,*,5"])
    assert before_rows == before_copy
    assert before_quote["total_cost"] == 4 * 300 + 900


def test_two_services_do_not_share_state():
    one, other = make(KETTLE), impl.ShippingService()
    assert other.list_rules() == (200, [])
    fails(404, "country_not_found", other.calculate_shipping, "NL", [])
    other.register_rules(["NL,kettle,fixed,1,*,1"])
    assert quote(one, "NL", ["kettle,1"])["total_cost"] == 300


# ---- 对照实现：逐件计价 ----

def naive_price(tiers, quantity):
    """不看公式，一件一件地买：每一件落进它所在的段；固定段只在第一件进入时收费。"""
    total, charged = 0, set()
    for unit in range(1, quantity + 1):
        for index, (kind, low, high, cost) in enumerate(tiers):
            if low <= unit and (high is None or unit <= high):
                if kind == "incremental":
                    total += cost
                elif index not in charged:
                    charged.add(index)
                    total += cost
    return total


@pytest.mark.parametrize("seed", range(12))
def test_random_schedules_match_the_unit_by_unit_oracle(seed):
    rng = random.Random(seed)
    tiers, start = [], 1
    for _ in range(rng.randint(1, 5)):
        width = rng.randint(1, 8)
        tiers.append((rng.choice(["incremental", "fixed"]), start, start + width - 1, rng.randint(1, 900)))
        start += width
    tiers.append((rng.choice(["incremental", "fixed"]), start, None, rng.randint(1, 900)))
    lines = [f"SE,box,{kind},{low},{'*' if high is None else high},{cost}" for kind, low, high, cost in tiers]
    rng.shuffle(lines)
    service = make(lines)
    for quantity in range(1, start + 12):
        split = rng.randint(1, quantity)
        got = quote(service, "SE", [f"box,{split}", f"box,{quantity - split}"] if split < quantity else [f"box,{quantity}"])
        assert got["total_cost"] == naive_price(tiers, quantity), (seed, quantity)
