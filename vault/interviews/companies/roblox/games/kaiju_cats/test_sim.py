"""One test per rule, each on a tiny board so the rule is the only thing happening.  python3 -m unittest test_sim -v"""
import unittest

from board import CHI_PLAN_MAP2, COST, GRASS as g, H, L, MAP1, MUD, P, ROCK, SPIKE
from sim import Rules, simulate

def run(board, plan=None, turns=15, **kw):
    return simulate(plan, Rules(turns=turns, **kw), board=board)


def cat(state, color):
    return next(k for k in state[1] if k[0] == color)


EMPTY = [g, g, g]


class Buildings(unittest.TestCase):
    def test_one_floor_per_visit_then_moves_on(self):
        _, st, _ = run([["start:R", H, g], ["start:G", *EMPTY], ["start:B", *EMPTY]], turns=2)
        self.assertEqual(cat(st, "R")[1:5], (0, 2, "E", 500))
        self.assertEqual(st[2][0], 1)  # one floor of the high building is left

    def test_second_visit_takes_the_bottom_floor_and_rubble_is_ground(self):
        # R goes E through L, bounces off the edge, comes back W through L (bottom floor), then rubble next pass
        _, st, _ = run([["start:R", L, g], ["start:G", *EMPTY], ["start:B", *EMPTY]], turns=6)
        self.assertEqual(st[2][0], 0)
        self.assertEqual(cat(st, "R")[4], 500)

    def test_power_plant_doubles(self):
        _, st, _ = run([["start:R", H, P], ["start:G", *EMPTY], ["start:B", *EMPTY]], turns=2)
        self.assertEqual(cat(st, "R")[4], 1000)


class Obstacles(unittest.TestCase):
    def test_mud_stuck_one_turn_then_same_direction(self):
        board = [["start:R", MUD, g, g], ["start:G", g, g, g], ["start:B", g, g, g]]
        _, st, _ = run(board, turns=2)
        self.assertEqual(cat(st, "R")[1:3], (0, 1))  # turn 2 stuck
        _, st, _ = run(board, turns=3)
        self.assertEqual(cat(st, "R")[1:4], (0, 2, "E"))

    def test_spike_halves_and_keeps_going(self):
        _, st, _ = run([["start:R", H, SPIKE, g], ["start:G", *EMPTY], ["start:B", *EMPTY]], turns=3)
        self.assertEqual(cat(st, "R")[1:5], (0, 3, "E", 250))

    def test_boulder_rebound_stay(self):
        board = [["start:R", g, ROCK], ["start:G", *EMPTY], ["start:B", *EMPTY]]
        _, st, _ = run(board, turns=2, rebound="stay")
        self.assertEqual(cat(st, "R")[1:4], (0, 1, "W"))

    def test_boulder_rebound_step(self):
        board = [["start:R", g, ROCK], ["start:G", *EMPTY], ["start:B", *EMPTY]]
        _, st, _ = run(board, turns=2, rebound="step")
        self.assertEqual(cat(st, "R")[1:4], (0, 0, "W"))

    def test_edge_and_missing_tile_rebound_like_boulder(self):
        _, st, _ = run([["start:R", g, None], ["start:G", g], ["start:B", g]], turns=2)
        self.assertEqual(cat(st, "R")[1:4], (0, 1, "W"))
        self.assertEqual(cat(st, "G")[1:4], (1, 1, "W"))

    def test_other_cats_bed_blocks(self):
        _, st, _ = run([["start:R", g, "bed:G"], ["start:G", *EMPTY], ["start:B", *EMPTY]], turns=2)
        self.assertEqual(cat(st, "R")[1:4], (0, 1, "W"))


class Commands(unittest.TestCase):
    def test_turn_command_fires_on_destroy(self):
        board = [["start:R", L, g], [None, g, g], ["start:G", *EMPTY], ["start:B", *EMPTY]]
        _, st, _ = run(board, {(0, 1, 0): "S"}, turns=2)
        self.assertEqual(cat(st, "R")[1:5], (1, 1, "S", 250))

    def test_command_fires_for_whichever_cat_destroys_the_floor(self):
        # R takes the top floor; G later... simpler: plan on the BOTTOM floor fires for the second visitor
        board = [["start:R", L, g], ["start:G", *EMPTY], ["start:B", *EMPTY]]
        _, st, _ = run(board, {(0, 1, 1): "E"}, turns=5)  # R comes back W, destroys bottom, turned E again
        self.assertEqual(cat(st, "R")[1:4], (0, 2, "E"))

    def test_stomp_stays_and_takes_the_next_floor(self):
        board = [["start:R", H, g], ["start:G", *EMPTY], ["start:B", *EMPTY]]
        _, st, _ = run(board, {(0, 1, 0): "stomp"}, turns=2)
        self.assertEqual(cat(st, "R")[1:3], (0, 1))
        self.assertEqual(cat(st, "R")[4], 1000)
        self.assertEqual(st[2][0], 0)
        _, st, _ = run(board, {(0, 1, 0): "stomp"}, turns=3)
        self.assertEqual(cat(st, "R")[1:4], (0, 2, "E"))

    def test_powerup_adds_1000(self):
        _, st, _ = run([["start:R", L, g], ["start:G", *EMPTY], ["start:B", *EMPTY]], {(0, 1, 0): "powerup"}, turns=1)
        self.assertEqual(cat(st, "R")[4], 1250)

    def test_powerup_on_plant_order_is_a_switch(self):
        board = [["start:R", L, P], ["start:G", *EMPTY], ["start:B", *EMPTY]]
        plan = {(0, 2, 0): "powerup"}
        self.assertEqual(cat(run(board, plan, turns=2)[1], "R")[4], 1500)  # 250 x2 +1000
        self.assertEqual(cat(run(board, plan, turns=2, powerup_first=True)[1], "R")[4], 2500)  # (250+1000) x2

    def test_budget(self):
        with self.assertRaises(ValueError):
            run([["start:R", g], ["start:G", g], ["start:B", g]], {(9, 9, i): "powerup" for i in range(7)})


class FightsAndBeds(unittest.TestCase):
    def test_same_tile_higher_power_wins_loser_scores_zero(self):
        # R (row 0) is sent S onto row 1 at the moment G arrives there
        board = [["start:R", H, g], [None, g, g], ["start:G", L, g], ["start:B", *EMPTY]]
        _, st, _ = run(board, {(0, 1, 0): "S", (2, 1, 0): "N"}, turns=2)
        self.assertTrue(cat(st, "R")[6])
        self.assertFalse(cat(st, "G")[6])
        self.assertEqual(cat(st, "G")[4], 0)

    def test_tie_goes_to_topmost_bed(self):
        board = [["start:R", L, g], [None, g, g], ["start:G", L, g], ["start:B", *EMPTY]]
        _, st, _ = run(board, {(0, 1, 0): "S", (2, 1, 0): "N"}, turns=2)
        self.assertTrue(cat(st, "R")[6])
        self.assertFalse(cat(st, "G")[6])

    def test_head_on_swap_is_a_fight(self):
        # turn 1: R -> c1, G is blocked by the edge and turns W in place; turn 2: R -> c2 and G -> c1 cross head-on
        _, st, _ = run([["start:R", g, "start:G"], ["start:B", *EMPTY]], turns=2, rebound="stay")
        self.assertTrue(cat(st, "R")[6])  # tie at 0 power: R has the topmost bed
        self.assertFalse(cat(st, "G")[6])

    def test_moving_into_a_stationary_cat_is_a_fight(self):
        # G sits stuck in mud at r1c1 on turn 2; R is turned S by the command and walks onto it
        board = [["start:R", H, g], ["start:G", MUD, g], ["start:B", *EMPTY]]
        _, st, _ = run(board, {(0, 1, 0): "S"}, turns=2)
        self.assertEqual(cat(st, "R")[1:3], (1, 1))
        self.assertFalse(cat(st, "G")[6])

    def test_bed_bonus_order_and_simultaneous_lower_first(self):
        board = [["start:R", H, "bed:R"], ["start:G", L, "bed:G"], ["start:B", g, g, "bed:B"]]
        score, st, _ = run(board, turns=4)
        # turn 2: R (500) and G (250) arrive together: G first +2000, R second x3; turn 4: B (0) third x5
        self.assertEqual(cat(st, "G")[4], 2250)
        self.assertEqual(cat(st, "R")[4], 1500)
        self.assertEqual(cat(st, "B")[4], 0)
        self.assertEqual(score, 3750)

    def test_cats_outside_beds_still_score_dead_ones_do_not(self):
        score, _, _ = run([["start:R", H, g], ["start:G", H, g], ["start:B", H, g]], turns=3)
        self.assertEqual(score, 1500)
        board = [["start:R", H, g], [None, g, g], ["start:G", L, g], ["start:B", *EMPTY]]
        score, _, _ = run(board, {(0, 1, 0): "S", (2, 1, 0): "N"}, turns=2)
        self.assertEqual(score, 500)  # G (250) died in the fight


class RealBoards(unittest.TestCase):
    def test_map1_no_commands(self):
        score, st, _ = simulate(board=MAP1)
        self.assertEqual([k[1:3] for k in st[1]], [(2, 3), (4, 3), (0, 3)])
        self.assertEqual(score, 406.25 + 2500 + 3000)

    def test_chi_plan_map2_fits_the_budget(self):
        self.assertEqual(sum(COST[c] for c in CHI_PLAN_MAP2.values()), 110)


if __name__ == "__main__":
    unittest.main()
