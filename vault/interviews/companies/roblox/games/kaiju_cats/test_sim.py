"""One test per rule. Cats not under test start boxed in (a missing tile on both sides) so they never move."""
import json
import os
import unittest
from dataclasses import replace

from sim import BOARD_A, BOARD_B, COST, Game, Rules, simulate

IDLE_G = ["startG", None]
IDLE_B = ["startB", None]


def run(rows, turns, plan=None, rules=Rules()):
    """rows may omit idle cats; returns ({color: cat tuple}, trace of states)."""
    colors = {cell[-1] for row in rows for cell in row if isinstance(cell, str) and cell.startswith("start")}
    board = rows + ([IDLE_G] if "G" not in colors else []) + ([IDLE_B] if "B" not in colors else [])
    trace = []
    _, state = simulate(plan, replace(rules, turns=turns), board, trace)
    return {k[0]: k for k in state[1]}, trace


# cat tuple fields
R_, C_, D_, P_, OUT = 1, 2, 3, 4, 7


class RuleTests(unittest.TestCase):
    def test_one_floor_per_visit_then_move_on(self):
        cats, trace = run([["startR", "L", "grass"]], 2)
        self.assertEqual([t[1][0][P_] for t in trace], [250, 250])
        self.assertEqual(cats["R"][C_], 2)

    def test_second_visit_takes_the_next_floor(self):
        # t1 enters L (250), t2 walks on, t3 bounces off the boulder, t4 walks back into L for its bottom floor.
        _, trace = run([["startR", "L", "grass", "boulder"]], 4)
        self.assertEqual([(t[1][0][C_], t[1][0][P_]) for t in trace], [(1, 250), (2, 250), (2, 250), (1, 500)])

    def test_stomp_waits_and_destroys_the_next_floor(self):
        _, trace = run([["startR", "L", "grass"]], 3, plan={(0, 1, 0): "stomp"})
        self.assertEqual([(t[1][0][C_], t[1][0][P_]) for t in trace], [(1, 250), (1, 500), (2, 500)])

    def test_stomp_on_the_last_floor_just_waits(self):
        _, trace = run([["startR", "P", "grass"]], 2, plan={(0, 1, 0): "stomp"})
        self.assertEqual([t[1][0][C_] for t in trace], [1, 1])

    def test_alternative_stay_until_gone(self):
        cats, _ = run([["startR", "H", "grass"]], 3, rules=Rules(entry_mode="stay_until_gone"))
        self.assertEqual((cats["R"][C_], cats["R"][P_]), (2, 1000))

    def test_alternative_all_on_entry(self):
        cats, _ = run([["startR", "H", "grass"]], 1, rules=Rules(entry_mode="all_on_entry"))
        self.assertEqual(cats["R"][P_], 1000)

    def test_power_plant_doubles_current_power(self):
        cats, _ = run([["startR", "H", "P", "grass"]], 2)
        self.assertEqual(cats["R"][P_], 1000)  # 500, then x2

    def test_mud_holds_for_one_turn_then_same_direction(self):
        _, trace = run([["startR", "mud", "grass"]], 3)
        self.assertEqual([t[1][0][C_] for t in trace], [1, 1, 2])

    def test_spike_halves_power_and_keeps_moving(self):
        cats, _ = run([["startR", "H", "spike", "grass"]], 3)
        self.assertEqual((cats["R"][C_], cats["R"][P_]), (3, 250))

    def test_boulder_rebounds(self):
        _, trace = run([["startR", "grass", "boulder"]], 3)
        self.assertEqual([(t[1][0][C_], t[1][0][D_]) for t in trace], [(1, "E"), (1, "W"), (0, "W")])

    def test_turn_command_fires_when_its_floor_is_destroyed(self):
        rows = [["startR", "L", None], [None, "grass", None]]
        cats, _ = run(rows, 2, plan={(0, 1, 0): "S"})
        self.assertEqual((cats["R"][R_], cats["R"][C_]), (1, 1))

    def test_budget_is_enforced(self):
        with self.assertRaises(ValueError):
            simulate({(r, c, 0): "stomp" for r in range(5) for c in range(1, 3)} | {(0, 1, 1): "stomp"})
        g = Game(rules=Rules(budget=5))
        self.assertIsNone(g.step(g.initial, lambda c, fid, m: "N" if c == "R" else None))

    def test_paid_command_applies_without_charge(self):
        g = Game([["startR", "L", None], [None, "grass", None], IDLE_G, IDLE_B], Rules(budget=0))
        s = g.step(g.initial, lambda c, fid, m: ("paid", "S") if c == "R" else None)
        self.assertEqual((s[1][0][D_], s[4]), ("S", 0))

    def test_bed_bonuses_by_arrival_order(self):
        rows = [["startR", "bedR"], ["startG", "grass", "bedG"], ["startB", "grass", "grass", "bedB"]]
        cats, _ = run(rows, 3)
        self.assertEqual((cats["R"][P_], cats["G"][P_], cats["B"][P_]), (2000, 0, 0))

    def test_simultaneous_arrival_lower_score_enters_first(self):
        rows = [["startR", "L", "bedR"], ["startG", "H", "bedG"]]
        cats, _ = run(rows, 2)
        self.assertEqual((cats["R"][P_], cats["G"][P_]), (2250, 1500))  # R 250 first (+2000), G 500 second (x3)

    def test_fight_on_one_tile_higher_power_wins(self):
        # R smashes H (500) and walks east; G bounces off the east edge and walks west; both reach c3 on turn 3.
        cats, _ = run([["startR", "H", "grass", "grass", "grass", "startG"]], 3)
        self.assertEqual((cats["G"][OUT], cats["R"][OUT]), ("out", ""))

    def test_fight_tie_top_bed_wins(self):
        cats, _ = run([["startR", "grass", "grass", "startG"]], 2)  # both 0 power meet at c2 on turn 2
        self.assertEqual((cats["G"][OUT], cats["R"][OUT]), ("out", ""))

    def test_head_on_swap_is_a_fight(self):
        # Turn 1: R -> c1, G bounces at c2 (now facing west). Turn 2: they cross head-on.
        cats, _ = run([["startR", "grass", "startG"]], 2)
        self.assertEqual((cats["G"][OUT], cats["R"][OUT], cats["R"][C_]), ("out", "", 2))

    def test_alternative_absorb_adds_loser_power(self):
        rows = [["startR", "H", "grass", "grass", "L", "startG"]]  # R 500 meets G 250 at c3 on turn 3
        cats, _ = run(rows, 3, rules=Rules(fight_mode="absorb"))
        self.assertEqual((cats["G"][OUT], cats["R"][P_]), ("out", 750))


class BoardTests(unittest.TestCase):
    def test_baselines_without_commands(self):
        self.assertEqual(simulate(board=BOARD_B)[0], 6250)
        self.assertEqual(simulate(board=BOARD_A)[0], 6187.5)

    def test_best_known_plan_reproduces_its_score(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_plan.json")) as fh:
            data = json.load(fh)
        plan = {tuple(k): v for k, v in data["plan"]}
        self.assertLessEqual(sum(COST[v] for v in plan.values()), 200)
        self.assertEqual(simulate(plan)[0], data["score"])


if __name__ == "__main__":
    unittest.main()
