"""One test per rule on a tiny line.  python3 -m unittest test_factory -v"""
import unittest

from factory import Rules, backward_fill, load, optimize, simulate, topo


def level(nodes, hours=4, buff_cost=None):
    lv = {"hours": hours, "start_cash": 0, "nodes": nodes, "buff_cost": buff_cost or {}}
    for n in nodes.values():
        n.setdefault("inputs", {}); n.setdefault("period", 1); n.setdefault("unit_cost", 0)
        n.setdefault("price", 0); n.setdefault("max_rate", 50); n.setdefault("buffs", [])
    lv["order"] = topo(nodes)
    return lv


def setting(lv, **over):
    s = {n: (lv["nodes"][n]["rate"], frozenset()) for n in lv["nodes"]}
    for n, v in over.items():
        s[n] = v if isinstance(v, tuple) else (v, frozenset())
    return s


LINE = {"ore": {"rate": 10, "unit_cost": 1}, "shop": {"rate": 10, "inputs": {"ore": 1}, "price": 5}}


class Rules_(unittest.TestCase):
    def test_raw_is_paid_every_hour_used_or_not(self):
        lv = level(LINE)
        # 4 hours of ore (40 x $1); the shop sells from hour 1: 3 batches x 10 x $5
        self.assertEqual(simulate(lv, setting(lv)), -40 + 150)

    def test_same_hour_switch_removes_the_one_hour_lag(self):
        lv = level(LINE)
        self.assertEqual(simulate(lv, setting(lv), Rules(same_hour=True)), -40 + 200)

    def test_all_or_nothing_batch_waits_partial_does_not(self):
        lv = level({"ore": {"rate": 6}, "shop": {"rate": 10, "inputs": {"ore": 1}, "price": 1}}, hours=5)
        # all: stock 6, 12 -> batch of 10 at hour 2, stock 2+6=8 at 3, 14 at 4 -> batch: 20 sold
        self.assertEqual(simulate(lv, setting(lv)), 20)
        # partial: 6 at hours 1..4 = 24
        self.assertEqual(simulate(lv, setting(lv), Rules(batch="partial")), 24)

    def test_two_hour_machine_delivers_after_two_hours(self):
        lv = level({"ore": {"rate": 10}, "jam": {"rate": 20, "period": 2, "inputs": {"ore": 1}},
                    "shop": {"rate": 10, "inputs": {"jam": 1}, "price": 1}}, hours=6)
        # jam can start at hour 2 (20 ore in stock), delivers 20 at hour 4; shop sells 10 at 4 and 10 at 5
        self.assertEqual(simulate(lv, setting(lv)), 20)

    def test_half_input_needs_half_and_is_charged_per_unit(self):
        lv = level({"ore": {"rate": 5}, "shop": {"rate": 10, "inputs": {"ore": 1}, "price": 1, "buffs": ["half_input"]}},
                   hours=3, buff_cost={"half_input": {"per_unit": 0.1}})
        s = setting(lv, shop=(10, frozenset({"half_input"})))
        self.assertAlmostEqual(simulate(lv, s), 2 * (10 - 1))  # hours 1 and 2, 10 each, minus $0.1 x 10

    def test_double_output_is_charged_on_every_unit(self):
        lv = level({"ore": {"rate": 10}, "shop": {"rate": 10, "inputs": {"ore": 1}, "price": 1, "buffs": ["double_output"]}},
                   hours=2, buff_cost={"double_output": {"per_unit": 0.4}})
        s = setting(lv, shop=(10, frozenset({"double_output"})))
        self.assertAlmostEqual(simulate(lv, s), 20 - 0.4 * 20)

    def test_fast_turns_two_hours_into_one_flat_fee(self):
        lv = level({"ore": {"rate": 20}, "jam": {"rate": 20, "period": 2, "inputs": {"ore": 1}, "buffs": ["fast"]},
                    "shop": {"rate": 20, "inputs": {"jam": 1}, "price": 1}}, hours=5, buff_cost={"fast": {"flat": 3}})
        s = setting(lv, jam=(20, frozenset({"fast"})))
        self.assertEqual(simulate(lv, s), 3 * 20 - 3)  # jam at 1,2,3 -> shop sells at 2,3,4

    def test_a_batch_finishing_after_the_last_hour_does_not_sell(self):
        lv = level({"ore": {"rate": 10}, "shop": {"rate": 10, "period": 2, "inputs": {"ore": 1}, "price": 1}}, hours=2)
        self.assertEqual(simulate(lv, setting(lv)), 0)

    def test_backward_fill_matches_downstream_demand(self):
        lv = level({"ore": {"rate": 1, "max_rate": 50}, "bar": {"rate": 1, "inputs": {"ore": 2}, "max_rate": 50},
                    "shop": {"rate": 1, "inputs": {"bar": 1}, "price": 9, "max_rate": 40}})
        s = backward_fill(lv)
        self.assertEqual(s["shop"][0], 25)  # ore caps at 50 = 2 x 25
        self.assertEqual(s["ore"][0], 50)

    def test_sandwich_example_runs_under_a_second(self):
        lv = load("sandwich_tutorial.json")
        cash, _ = optimize(lv, budget=1.0, log=lambda *a: None)
        self.assertGreater(cash, 0)


if __name__ == "__main__":
    unittest.main()
