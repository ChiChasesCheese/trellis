"""One test per rule of the in-game instructions, each on a tiny line.  python3 -m unittest test_factory -v"""
import unittest

from factory import backward_fill, given_setting, load, optimize, prepare, simulate


def run(nodes, hours=4, start=0, **over):
    lv = prepare({"hours": hours, "start_cash": start, "nodes": nodes})
    s = given_setting(lv)
    for n, v in over.items():
        s[n] = v
    trace = []
    return simulate(lv, s, trace), trace[-1]


def line(sup=10, make=10, sell=10, price=5, cost=1, **extra):
    return {"ore": {"kind": "supplier", "rate": sup, "unit_cost": cost},
            "bar": {"kind": "maker", "rate": make, "options": [{"inputs": {"ore": 1}}], **extra},
            "shop": {"kind": "seller", "rate": sell, "options": [{"name": "Bar", "inputs": {"bar": 1}, "price": price}]}}


class Timing(unittest.TestCase):
    def test_start_money_and_supplier_paid_every_hour(self):
        money, _ = run({"ore": {"kind": "supplier", "rate": 10, "unit_cost": 0.5}}, hours=3, start=3000)
        self.assertEqual(money, 3000 - 15)

    def test_orders_usable_at_once_made_items_next_hour(self):
        # ore at h0 -> bar made h0, in storage end of h0 -> shop sells h1, h2, h3
        money, end = run(line(), hours=4)
        self.assertEqual(end["sold"], {"Bar": 30})
        self.assertEqual(money, 30 * 5 - 40)

    def test_two_hour_machine_pulls_once_delivers_at_end_of_second_hour(self):
        nodes = line(make=20, sup=20)
        nodes["bar"]["options"][0]["period"] = 2
        _, end = run(nodes, hours=6, **{"shop": (20, 0, frozenset())})
        # bar runs h0-1, h2-3, h4-5; sells at h2 and h4 (the h4-5 batch lands at the end of h5, after the last pull)
        self.assertEqual(end["batches"]["bar"], 3)
        self.assertEqual(end["sold"], {"Bar": 40})


class Batches(unittest.TestCase):
    def test_not_enough_inputs_means_nothing_this_hour(self):
        _, end = run(line(sup=6, make=10, sell=10, cost=0), hours=6)
        # ore 6,12 -> bar at h1 (12-10=2), 8 no, 14 at h3 (4), 10 at h4 (0), 6 no
        self.assertEqual(end["batches"]["bar"], 3)

    def test_storage_full_items_are_lost_and_still_paid(self):
        nodes = line(sup=50, make=50, sell=0, cost=1)
        money, end = run(nodes, hours=3)
        self.assertEqual(end["left"]["bar"], 100)  # maker storage 100
        self.assertEqual(end["lost"]["bar"], 50)
        self.assertEqual(money, -150)

    def test_supplier_storage_1000(self):
        _, end = run({"ore": {"kind": "supplier", "rate": 600}}, hours=2)
        self.assertEqual(end["left"]["ore"], 1000)
        self.assertEqual(end["lost"]["ore"], 200)


class Priority(unittest.TestCase):
    def test_closest_to_seller_served_first_and_short_one_is_skipped(self):
        nodes = {
            "ore": {"kind": "supplier", "row": 0, "rate": 10},
            "far": {"kind": "maker", "row": 0, "rate": 10, "options": [{"inputs": {"ore": 1}}]},
            "mid": {"kind": "maker", "row": 1, "rate": 10, "options": [{"inputs": {"far": 1}}]},
            "near": {"kind": "seller", "row": 2, "rate": 8, "options": [{"name": "N", "inputs": {"ore": 1}, "price": 1}]},
            "end": {"kind": "seller", "row": 3, "rate": 1, "options": [{"name": "E", "inputs": {"mid": 1}, "price": 0}]},
        }
        _, end = run(nodes, hours=1)
        # 10 ore: the seller (distance 0) takes 8 first; "far" (distance 2) wants 10, finds 2, is skipped entirely
        self.assertEqual(end["batches"]["far"], 0)
        self.assertEqual(end["sold"]["N"], 8)

    def test_tie_goes_to_the_topmost(self):
        nodes = {
            "ore": {"kind": "supplier", "row": 0, "rate": 10},
            "low": {"kind": "seller", "row": 5, "rate": 10, "options": [{"name": "L", "inputs": {"ore": 1}, "price": 1}]},
            "top": {"kind": "seller", "row": 1, "rate": 10, "options": [{"name": "T", "inputs": {"ore": 1}, "price": 1}]},
        }
        _, end = run(nodes, hours=1)
        self.assertEqual(end["sold"], {"T": 10})


class Mods(unittest.TestCase):
    def test_half_materials_and_its_fee(self):
        nodes = line(sup=5, cost=0)
        nodes["bar"]["mods"] = {"half": 0.2}
        money, end = run(nodes, hours=3, bar=(10, 0, frozenset({"half"})))
        self.assertEqual(end["batches"]["bar"], 3)  # 5 ore per 10 bars
        self.assertAlmostEqual(money, 20 * 5 - 3 * 10 * 0.2)

    def test_output2x_raises_the_max_not_the_output(self):
        lv = prepare({"hours": 1, "nodes": line(**{"mods": {"output2x": 0.1}})})
        from factory import valid
        s = given_setting(lv)
        self.assertFalse(valid(lv, {**s, "bar": (80, 0, frozenset())}))
        self.assertTrue(valid(lv, {**s, "bar": (80, 0, frozenset({"output2x"}))}))

    def test_fast_makes_a_two_hour_machine_one_hour(self):
        nodes = line(make=10, cost=0)
        nodes["bar"]["options"][0]["period"] = 2
        nodes["bar"]["mods"] = {"fast": 0.5}
        _, end = run(nodes, hours=4, bar=(10, 0, frozenset({"fast"})))
        self.assertEqual(end["batches"]["bar"], 4)

    def test_product_option_changes_recipe_and_price(self):
        nodes = line(cost=0)
        nodes["shop"]["options"].append({"name": "Gold", "inputs": {"bar": 2}, "price": 20})
        money, _ = run(nodes, hours=3, shop=(5, 1, frozenset()))
        self.assertEqual(money, 2 * 5 * 20)


class Search(unittest.TestCase):
    def test_backward_fill_meets_demand_within_max(self):
        lv = prepare({"nodes": line()})
        s = backward_fill(lv, {"bar": 0, "shop": 0, "ore": 0}, {"shop"})
        self.assertEqual((s["ore"][0], s["bar"][0], s["shop"][0]), (50, 50, 50))

    def test_tutorial_level_optimizes_fast(self):
        lv = load("sandwich_tutorial.json")
        money, _ = optimize(lv, budget=2.0, log=lambda *a: None)
        self.assertGreater(money, 3828)


if __name__ == "__main__":
    unittest.main()
