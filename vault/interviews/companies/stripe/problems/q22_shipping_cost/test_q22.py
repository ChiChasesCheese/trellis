import random

import pytest

ROUTES = "US:UK:FedEx:5,UK:US:UPS:4,UK:CA:FedEx:7,US:CA:DHL:10,UK:FR:DHL:2"
ROUTES2 = "A:B:UPS:1,B:C:UPS:1,C:D:UPS:1,A:D:DHL:5,A:C:FedEx:1"

MATRIX = {
    "US": [{"product": "mouse", "cost": 550}, {"product": "laptop", "cost": 1000}],
    "CA": [{"product": "mouse", "cost": 750}, {"product": "laptop", "cost": 1100}],
}
TIERED = {
    "US": [
        {"product": "mouse", "cost": 550},
        {"product": "laptop", "tiers": [{"min": 1, "max": 2, "cost": 1000},
                                        {"min": 3, "max": 4, "cost": 950},
                                        {"min": 5, "max": None, "cost": 900}]},
    ],
    "CA": [
        {"product": "mouse", "cost": 750},
        {"product": "laptop", "tiers": [{"min": 1, "max": 2, "cost": 1100},
                                        {"min": 3, "max": None, "cost": 1000}]},
    ],
}
STRIPE_DOC_TIERS = [{"min": 1, "max": 5, "cost": 700}, {"min": 6, "max": None, "cost": 650}]
RACK = [{"min": 1, "max": 1, "flat": 2500}, {"min": 2, "max": None, "cost": 900}]


def order(country, *items):
    return {"country": country, "items": [{"product": p, "quantity": q} for p, q in items]}


def p2(impl, s, a, b):
    return impl.format_path(*impl.shipping_cost_one_transfer(impl.parse_routes(s), a, b))


def p3(impl, s, a, b):
    return impl.format_path(*impl.cheapest_shipping(impl.parse_routes(s), a, b))


# ---------------------------------------------------------------- Part 1: direct leg + carrier
@pytest.mark.part1
def test_example_direct(impl):
    r = impl.parse_routes(ROUTES)
    assert impl.shipping_cost(r, "US", "UK", "FedEx") == 5
    assert impl.shipping_cost(r, "US", "CA", "DHL") == 10
    assert impl.shipping_cost(r, "US", "CA", "FedEx") == -1
    assert impl.shipping_cost(r, "UK", "US", "UPS") == 4
    assert impl.shipping_cost(r, "US", "FR", "DHL") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_legs_are_directed_and_unknown_codes(impl):
    r = impl.parse_routes(ROUTES)
    assert impl.shipping_cost(r, "US", "UK", "UPS") == -1     # UK:US:UPS is the reverse leg
    assert impl.shipping_cost(r, "UK", "FR", "DHL") == 2
    assert impl.shipping_cost(r, "XX", "UK", "FedEx") == -1
    assert impl.shipping_cost(r, "US", "UK", "fedex") == -1   # case-sensitive
    assert impl.shipping_cost([], "US", "UK", "FedEx") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_parse_tolerates_spaces_and_alt_separators_and_duplicates(impl):
    r = impl.parse_routes(" US : UK : FedEx : 5 , UK:US:UPS:4 ")
    assert r == [impl.Route("US", "UK", "FedEx", 5), impl.Route("UK", "US", "UPS", 4)]
    r = impl.parse_routes("US,UK,UPS,5:US,CA,FedEx,3:CA,UK,DHL,7")
    assert impl.shipping_cost(r, "US", "CA", "FedEx") == 3
    # duplicate (src,dst,carrier): the cheaper leg wins
    r = impl.parse_routes("US:UK:FedEx:9,US:UK:FedEx:5,US:UK:FedEx:7")
    assert impl.shipping_cost(r, "US", "UK", "FedEx") == 5
    assert impl.parse_routes("") == []


# ---------------------------------------------------------------- Part 2: one transfer
@pytest.mark.part2
def test_example_one_transfer(impl):
    assert p2(impl, ROUTES, "US", "FR") == "7 US-FedEx->UK-DHL->FR"
    assert p2(impl, ROUTES, "US", "CA") == "10 US-DHL->CA"
    assert p2(impl, ROUTES, "CA", "US") == "-1"


@pytest.mark.part2
@pytest.mark.edge
def test_direct_preferred_over_cheaper_transfer(impl):
    assert p2(impl, ROUTES2, "A", "D") == "5 A-DHL->D"
    # three legs needed -> not allowed with one transfer
    assert p2(impl, "A:B:UPS:1,B:C:UPS:1,C:D:UPS:1", "A", "D") == "-1"


@pytest.mark.part2
@pytest.mark.fmt
def test_one_transfer_cheapest_and_tiebreak(impl):
    s = "A:X:UPS:3,X:B:UPS:3,A:Y:DHL:2,Y:B:DHL:2,A:Z:UPS:2,Z:B:UPS:2"
    # Y and Z both cost 4 -> lexicographically smaller path ['A','DHL','Y',...] < ['A','UPS','Z',...]
    assert p2(impl, s, "A", "B") == "4 A-DHL->Y-DHL->B"
    # cheapest direct among several carriers
    assert p2(impl, "A:B:UPS:6,A:B:DHL:4,A:B:FedEx:4", "A", "B") == "4 A-DHL->B"


@pytest.mark.part2
@pytest.mark.edge
def test_one_transfer_src_equals_dst_is_zero_not_a_loop(impl):
    r = impl.parse_routes(ROUTES)
    assert impl.shipping_cost_one_transfer(r, "US", "US") == (0, ["US"])  # not US->UK->US = 9
    assert p2(impl, ROUTES, "US", "US") == "0 US"
    assert p2(impl, "", "US", "US") == "0 US"


# ---------------------------------------------------------------- Part 3: cheapest path
@pytest.mark.part3
def test_example_cheapest(impl):
    assert p3(impl, ROUTES, "US", "FR") == "7 US-FedEx->UK-DHL->FR"
    assert p3(impl, ROUTES, "US", "CA") == "10 US-DHL->CA"
    assert p3(impl, ROUTES, "UK", "UK") == "0 UK"
    assert p3(impl, ROUTES2, "A", "D") == "2 A-FedEx->C-UPS->D"


@pytest.mark.part3
@pytest.mark.edge
def test_cheapest_unreachable_zero_cost_and_ties(impl):
    assert p3(impl, ROUTES, "CA", "US") == "-1"
    assert p3(impl, ROUTES, "US", "ZZ") == "-1"
    assert p3(impl, "A:B:UPS:0,B:C:UPS:0,A:C:DHL:0", "A", "C") == "0 A-DHL->C"  # fewer legs on tie
    # equal cost & legs -> lexicographically smaller path
    assert p3(impl, "A:B:UPS:1,B:D:UPS:1,A:C:DHL:1,C:D:DHL:1", "A", "D") == "2 A-DHL->C-DHL->D"


@pytest.mark.part3
@pytest.mark.edge
def test_cheapest_long_chain_beats_direct(impl):
    s = ",".join(f"N{i}:N{i+1}:UPS:1" for i in range(10)) + ",N0:N10:DHL:50"
    cost, path = impl.cheapest_shipping(impl.parse_routes(s), "N0", "N10")
    assert cost == 10 and path[0] == "N0" and path[-1] == "N10" and len(path) == 21


# ---------------------------------------------------------------- Part 4: flat matrix
@pytest.mark.part4
def test_example_matrix_verbatim(impl):
    assert impl.calculate_shipping_cost(order("US", ("mouse", 20), ("laptop", 5)), MATRIX) == 16000
    assert impl.calculate_shipping_cost(order("CA", ("mouse", 20), ("laptop", 5)), MATRIX) == 20500


@pytest.mark.part4
@pytest.mark.edge
def test_matrix_errors(impl):
    with pytest.raises(ValueError, match="unknown country 'FR'"):
        impl.calculate_shipping_cost(order("FR", ("mouse", 1)), MATRIX)
    with pytest.raises(ValueError, match="unknown product 'rack' for country 'US'"):
        impl.calculate_shipping_cost(order("US", ("rack", 1)), MATRIX)
    with pytest.raises(ValueError, match="negative quantity"):
        impl.calculate_shipping_cost(order("US", ("mouse", -1)), MATRIX)


@pytest.mark.part4
@pytest.mark.edge
def test_matrix_zero_empty_duplicates_and_dict_form(impl):
    assert impl.calculate_shipping_cost(order("US", ("mouse", 0)), MATRIX) == 0
    assert impl.calculate_shipping_cost(order("US"), MATRIX) == 0
    # same product twice in the order -> summed
    assert impl.calculate_shipping_cost(order("US", ("mouse", 2), ("mouse", 3)), MATRIX) == 2750
    # product listed twice in the matrix -> last wins
    m = {"US": [{"product": "mouse", "cost": 1}, {"product": "mouse", "cost": 550}]}
    assert impl.calculate_shipping_cost(order("US", ("mouse", 1)), m) == 550
    # dict form of the matrix
    assert impl.calculate_shipping_cost(order("US", ("mouse", 2)), {"US": {"mouse": 550}}) == 1100
    assert impl.calculate_shipping_cost(order("US", ("mouse", 2)), {"US": {"mouse": {"cost": 550}}}) == 1100


@pytest.mark.part4
@pytest.mark.edge
def test_matrix_huge_quantity_is_exact(impl):
    assert impl.calculate_shipping_cost(order("US", ("laptop", 10**12)), MATRIX) == 10**15


# ---------------------------------------------------------------- Part 5: tiers
@pytest.mark.part5
def test_example_tiers_repo_data(impl):
    us, ca = order("US", ("mouse", 20), ("laptop", 5)), order("CA", ("mouse", 20), ("laptop", 5))
    assert impl.calculate_shipping_cost(us, TIERED, mode="volume") == 15500
    assert impl.calculate_shipping_cost(ca, TIERED, mode="volume") == 20000
    assert impl.calculate_shipping_cost(us, TIERED, mode="graduated") == 15800
    assert impl.calculate_shipping_cost(ca, TIERED, mode="graduated") == 20200


@pytest.mark.part5
def test_stripe_docs_numbers(impl):
    m = {"US": [{"product": "seat", "tiers": STRIPE_DOC_TIERS}]}
    assert impl.calculate_shipping_cost(order("US", ("seat", 6)), m, mode="graduated") == 4150  # 5*7 + 1*6.5
    assert impl.calculate_shipping_cost(order("US", ("seat", 6)), m, mode="volume") == 3900     # 6*6.5


@pytest.mark.part5
@pytest.mark.edge
def test_tier_boundaries_inclusive(impl):
    m = {"US": [{"product": "seat", "tiers": STRIPE_DOC_TIERS}]}
    for qty, grad, vol in [(4, 2800, 2800), (5, 3500, 3500), (6, 4150, 3900), (7, 4800, 4550), (0, 0, 0)]:
        assert impl.calculate_shipping_cost(order("US", ("seat", qty)), m, mode="graduated") == grad, qty
        assert impl.calculate_shipping_cost(order("US", ("seat", qty)), m, mode="volume") == vol, qty
    # repo laptop bands graduated/volume: 2 -> 2000/2000 ; 3 -> 2950/2850 ; 4 -> 3900/3800 ; 5 -> 4800/4500
    lap = {"US": [TIERED["US"][1]]}
    assert [impl.calculate_shipping_cost(order("US", ("laptop", q)), lap, mode="graduated") for q in (2, 3, 4, 5)] == [2000, 2950, 3900, 4800]
    assert [impl.calculate_shipping_cost(order("US", ("laptop", q)), lap, mode="volume") for q in (2, 3, 4, 5)] == [2000, 2850, 3800, 4500]


@pytest.mark.part5
@pytest.mark.edge
def test_flat_bands_and_closed_last_band(impl):
    m = {"US": [{"product": "rack", "tiers": RACK}]}
    assert impl.calculate_shipping_cost(order("US", ("rack", 1)), m, mode="volume") == 2500
    assert impl.calculate_shipping_cost(order("US", ("rack", 1)), m, mode="graduated") == 2500
    assert impl.calculate_shipping_cost(order("US", ("rack", 3)), m, mode="graduated") == 4300
    assert impl.calculate_shipping_cost(order("US", ("rack", 3)), m, mode="volume") == 2700
    assert impl.calculate_shipping_cost(order("US", ("rack", 0)), m, mode="graduated") == 0
    closed = {"US": [{"product": "x", "tiers": [{"min": 1, "max": 3, "cost": 10}]}]}
    with pytest.raises(ValueError, match="no tier"):
        impl.calculate_shipping_cost(order("US", ("x", 4)), closed, mode="graduated")
    with pytest.raises(ValueError, match="no tier"):
        impl.calculate_shipping_cost(order("US", ("x", 4)), closed, mode="volume")


@pytest.mark.part5
@pytest.mark.edge
def test_same_product_twice_is_merged_before_tiering(impl):
    m = {"US": [{"product": "seat", "tiers": STRIPE_DOC_TIERS}]}
    # 3 + 3 = 6 units -> graduated 4150 (not 2 x 2100 = 4200); volume 3900 (not 4200)
    assert impl.calculate_shipping_cost(order("US", ("seat", 3), ("seat", 3)), m, mode="graduated") == 4150
    assert impl.calculate_shipping_cost(order("US", ("seat", 3), ("seat", 3)), m, mode="volume") == 3900


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_routes_exact(run_script):
    r = run_script(f"PART 2\n{ROUTES}\nUS FR\nUS CA\nCA US\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7 US-FedEx->UK-DHL->FR\n10 US-DHL->CA\n-1\n"
    r = run_script(f"PART 1\n{ROUTES}\nUS UK FedEx\nUS CA FedEx\n")
    assert r.stdout == "5\n-1\n"
    r = run_script(f"PART 3\n{ROUTES2}\nA D\nD A\n")
    assert r.stdout == "2 A-FedEx->C-UPS->D\n-1\n"


@pytest.mark.part5
@pytest.mark.io
def test_stdin_matrix_exact(run_script):
    r = run_script("PART 4\nMATRIX\nUS mouse 550\nUS laptop 1000\nCA mouse 750\nCA laptop 1100\n"
                   "ORDER US\nmouse 20\nlaptop 5\nORDER CA\nmouse 20\nlaptop 5\nORDER FR\nmouse 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "16000\n20500\nERROR: unknown country 'FR'\n"
    r = run_script("PART 5\nMODE graduated\nMATRIX\nUS laptop 1-2:1000 3-4:950 5-:900\nUS rack 1-1:=2500 2-:900\n"
                   "ORDER US\nlaptop 6\nrack 3\nORDER US\nlaptop 6\n")
    assert r.stdout == "10000\n5700\n"
    r = run_script("PART 5\nMODE volume\nMATRIX\nUS seat 1-5:700 6-:650\nORDER US\nseat 6\n")
    assert r.stdout == "3900\n"
    assert run_script("").stdout == ""


@pytest.mark.part5
@pytest.mark.perf
def test_perf_100k_order_lines_and_20k_dijkstra_queries(run_script):
    rng = random.Random(0)
    lines = ["PART 5", "MODE graduated", "MATRIX"]
    products = [f"p{i}" for i in range(50)]
    for c in range(20):
        for p in products:
            lines.append(f"C{c} {p} 1-10:{rng.randrange(100, 1000)} 11-100:{rng.randrange(50, 100)} 101-:{rng.randrange(1, 50)}")
    for _ in range(1000):
        lines.append(f"ORDER C{rng.randrange(20)}")
        lines += [f"{rng.choice(products)} {rng.randrange(0, 500)}" for _ in range(100)]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 1000 and "ERROR" not in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    # route version: 60 countries, ~600 legs, 20k cheapest-path queries
    countries = [f"K{i}" for i in range(60)]
    legs = ",".join(f"{rng.choice(countries)}:{rng.choice(countries)}:{rng.choice(['UPS', 'DHL', 'FedEx'])}:{rng.randrange(1, 20)}" for _ in range(600))
    q = [f"{rng.choice(countries)} {rng.choice(countries)}" for _ in range(20_000)]
    r = run_script("PART 3\n" + legs + "\n" + "\n".join(q) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 20_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
