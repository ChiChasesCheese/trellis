"""One test per rule. Cats not under test start boxed in (a missing tile on both sides) so they never move."""
import unittest

from sim import BOARD, Rules, simulate
from solve import search

IDLE_G = ["startG", None]
IDLE_B = ["startB", None]


def run(row_r, turns, rows=None, plan=None, rules=None):
    board = rows or [row_r, IDLE_G, IDLE_B]
    trace = []
    rules = rules or Rules()
    rules = Rules(rules.entry_mode, rules.fight_mode, turns, rules.budget, rules.cost_per_command)
    score, cats, events = simulate(plan, rules, board, trace)
    return {k.color: k for k in cats}, trace, events


class RuleTests(unittest.TestCase):
    def test_building_one_floor_per_turn_then_move_on(self):
        cats, trace, _ = run(["startR", ("L",), "grass"], 3)
        self.assertEqual([t[1][0][4] for t in trace], [250, 500, 500])
        self.assertEqual((cats["R"].r, cats["R"].c), (0, 2))

    def test_all_on_entry_mode(self):
        cats, _, _ = run(["startR", ("H",), "grass"], 1, rules=Rules(entry_mode="all_on_entry"))
        self.assertEqual(cats["R"].power, 1000)

    def test_power_plant_doubles_current_power(self):
        cats, _, _ = run(["startR", ("L",), ("P",), "grass"], 3)
        self.assertEqual(cats["R"].power, 1000)  # 250, 500, then x2

    def test_mud_holds_for_one_turn_then_same_direction(self):
        _, trace, _ = run(["startR", "mud", "grass"], 3)
        self.assertEqual([t[1][0][2] for t in trace], [1, 1, 2])

    def test_spike_halves_power_and_keeps_moving(self):
        cats, trace, _ = run(["startR", ("H",), "spike", "grass"], 4)
        self.assertEqual(cats["R"].power, 500)
        self.assertEqual(cats["R"].c, 3)

    def test_boulder_rebounds(self):
        _, trace, _ = run(["startR", "grass", "boulder"], 3)
        self.assertEqual([(t[1][0][2], t[1][0][3]) for t in trace], [(1, "E"), (1, "W"), (0, "W")])

    def test_command_fires_when_its_floor_is_destroyed(self):
        board = [["startR", ("L", None, "S"), None], [None, "grass", None], IDLE_G, IDLE_B]
        cats, _, _ = run(None, 3, rows=board)
        self.assertEqual((cats["R"].r, cats["R"].c), (1, 1))

    def test_plan_overrides_a_floor(self):
        board = [["startR", ("L",), None], [None, "grass", None], IDLE_G, IDLE_B]
        cats, _, _ = run(None, 3, rows=board, plan={(0, 1, 1): "S"})
        self.assertEqual((cats["R"].r, cats["R"].c), (1, 1))

    def test_bed_bonuses_by_arrival_order(self):
        board = [["startR", "bedR"], ["startG", "grass", "bedG"], ["startB", "grass", "grass", "bedB"]]
        cats, _, _ = run(None, 3, rows=board)
        self.assertEqual(cats["R"].power, 2000)  # first: +2000
        self.assertEqual(cats["G"].power, 0)  # second: x3 of 0
        self.assertEqual(cats["B"].power, 0)

    def test_simultaneous_arrival_lower_score_enters_first(self):
        board = [["startR", ("L",), "bedR"], ["startG", ("H",), "bedG"], ["startB", None]]
        cats, _, _ = run(None, 3, rows=board)
        # R (500) and G (1000) reach their beds on turn 3; R is lower so it is first (+2000), G second (x3).
        self.assertEqual(cats["R"].power, 2500)
        self.assertEqual(cats["G"].power, 3000)

    def test_fight_higher_power_wins(self):
        # G bounces off the east edge on turn 1, then walks west; R smashes the H building and meets G at c2 on turn 3.
        cats, _, _ = run(None, 3, rows=[["startR", ("H",), "grass", "grass", "startG"], IDLE_B])
        self.assertTrue(cats["G"].out)
        self.assertEqual(cats["R"].power, 1000)

    def test_fight_tie_top_bed_wins(self):
        # Both at 0 power meet at c2 on turn 2; R's bed is the topmost, so R wins the tie.
        cats, _, _ = run(None, 2, rows=[["startR", "grass", "grass", "startG"], IDLE_B])
        self.assertTrue(cats["G"].out)
        self.assertFalse(cats["R"].out)

    def test_head_on_swap_is_a_fight(self):
        # Turn 1: R -> c1; G bounces off the east edge (stays at c2, now facing west).
        # Turn 2: R -> c2 and G -> c1 cross head-on: they fight, and R wins the 0-0 tie (topmost bed).
        cats, _, _ = run(None, 2, rows=[["startR", "grass", "startG"], IDLE_B])
        self.assertTrue(cats["G"].out)
        self.assertFalse(cats["R"].out)
        self.assertEqual(cats["R"].c, 2)

    def test_absorb_mode_adds_loser_power(self):
        # R smashes H (1000) and walks east; G bounces, smashes L (500) and walks west; they meet at c3 on turn 4.
        rows = [["startR", ("H",), "grass", "grass", ("L",), "startG"], IDLE_B]
        cats, _, _ = run(None, 4, rows=rows, rules=Rules(fight_mode="absorb"))
        self.assertTrue(cats["G"].out)
        self.assertEqual(cats["R"].power, 1500)


class BoardTests(unittest.TestCase):
    def test_baseline_without_commands(self):
        self.assertEqual(simulate()[0], 12500)

    def test_search_one_and_two_commands(self):
        self.assertEqual(search(max_commands=1)[0], 14000)
        self.assertEqual(search(max_commands=2)[0], 18000)


if __name__ == "__main__":
    unittest.main()
