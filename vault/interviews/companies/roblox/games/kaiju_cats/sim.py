"""Kaiju Cats (Roblox's official practice assessment game) — a simulator built from the in-game instructions.

Rules the instructions state are implemented as written. Rules they do not state are naive assumptions, each one named
in ASSUMPTIONS below and switchable through `Rules`, so a result can be re-run under a different reading.
"""
from __future__ import annotations

from dataclasses import dataclass

DIRS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
REVERSE = {"N": "S", "S": "N", "E": "W", "W": "E"}
BED_RANK = {"R": 0, "G": 1, "B": 2}  # top bed beats middle beats bottom (stated tie-break in fights)
COST = {"N": 10, "S": 10, "E": 10, "W": 10, "stomp": 20, "powerup": 30}  # command panel, 2026-09-28

ASSUMPTIONS = """
A1 Cats start with 0 power (the beds show 0 before any test) and face east.
A2 Each turn every cat acts once, all at the same time: it moves one tile, or stays if stuck or stomping.
A3 Entering a building destroys its top floor; next turn the cat moves on and the rest of the building stays
   (entry_mode="one_floor_per_visit"). Reason: the Stomp command ("that cat will wait and stomp again next turn")
   only makes sense if cats do not stay by default. Chi confirmed floors fall one at a time ("逐层拆").
   Alternatives kept for comparison: "stay_until_gone", "all_on_entry".
A4 A floor's command fires when that floor is destroyed: a turn command sets the direction; Stomp makes the cat stay
   next turn and destroy the next floor of the same building (if none is left, it just waits).
A5 Walls, missing tiles, a boulder and another cat's bed block: the cat stays this turn and reverses direction.
A6 Two cats on one tile fight, and so do two cats that swap tiles head-on; the loser is out and its power is lost.
   CONFIRMED by Chi ("会撞死一个").
A7 Power Up ($30): effect not yet known; the search leaves it out until its description is transcribed.
A8 Every command on the board is bought from the $200 budget; the board starts with none.
A9 After 15 turns the score is the sum of the powers of the cats still in play, in a bed or not.
"""


@dataclass(frozen=True)
class Rules:
    entry_mode: str = "one_floor_per_visit"  # or "stay_until_gone" | "all_on_entry"
    fight_mode: str = "eliminate"  # or "absorb"
    turns: int = 15
    budget: int = 200


# Board legend. H = high value (2 x 500), L = low value (2 x 250), P = power plant (1 floor, x2).
# BOARD_B: the board from Chi's second photo (2026-09-28), with Chi's own draft commands removed.
BOARD_B = [
    # c0        c1       c2        c3       c4         c5       c6
    ["startB", "L",     "L",      "grass", "H",       "P",     None],
    [None,     "L",     "spike",  "L",     "grass",   "P",     "bedR"],
    ["startR", "L",     "L",      "grass", "boulder", "H",     "bedG"],
    [None,     "H",     "P",      "mud",   "grass",   "H",     "bedB"],
    ["startG", "H",     "L",      "grass", "L",       "L",     None],
]
# BOARD_A: the board from Chi's first photo (a different layout), empty.
BOARD_A = [
    ["startB", "L",     "L",      "H",       "L",     "grass", None],
    [None,     "grass", "mud",    "P",       "H",     "L",     "bedR"],
    ["startR", "H",     "L",      "grass",   "spike", "H",     "bedG"],
    [None,     "grass", "P",      "boulder", "L",     "L",     "bedB"],
    ["startG", "H",     "L",      "grass",   "P",     "L",     None],
]
BOARD = BOARD_B

FLOOR_VALUE = {"H": 500, "L": 250, "P": "x2"}
FLOORS = {"H": 2, "L": 2, "P": 1}


def parse(board):
    """-> (kind grid dict, starts, building list). Buildings are indexed; floors[i] counts floors left."""
    kinds, starts, buildings = {}, {}, []
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell is None:
                continue
            if cell in FLOORS:
                kinds[(r, c)] = ("building", len(buildings))
                buildings.append(((r, c), cell))
            elif cell.startswith("start"):
                kinds[(r, c)] = ("grass", None)
                starts[cell[-1]] = (r, c)
            elif cell.startswith("bed"):
                kinds[(r, c)] = ("bed", cell[-1])
            else:
                kinds[(r, c)] = (cell, None)
    return kinds, starts, buildings


class Game:
    """Simulator over plain-tuple states so search can hash and copy them cheaply.

    state = (turn, cats, floors_left, arrivals, money)
    cat   = (color, r, c, d, power, stuck, stomp, status)   status: "" | "bed" | "out"
    """

    def __init__(self, board=BOARD, rules: Rules = Rules(), colors=("R", "G", "B")):
        self.rules = rules
        self.kinds, starts, self.buildings = parse(board)
        cats = tuple((col, *starts[col], "E", 0, 0, 0, "") for col in colors)
        floors = tuple(FLOORS[kind] for _, kind in self.buildings)
        self.initial = (0, cats, floors, 0, rules.budget)

    def floor_id(self, b, floors_left):
        """(r, c, floor index from the top) of the floor about to be destroyed in building b."""
        (r, c), kind = self.buildings[b]
        return (r, c, FLOORS[kind] - floors_left)

    def step(self, state, choose):
        """Advance one turn. `choose(cat_color, floor_id, money)` returns the command on the floor being destroyed
        (None for no command). Returns the next state, or None if a choice exceeds the budget."""
        turn, cats, floors, arrivals, money = state
        cats = [list(k) for k in cats]
        floors = list(floors)
        rules = self.rules
        moved, origin = [], {}

        smash_now = []  # cats that destroy a floor this turn without moving (stomp / stay_until_gone)
        for k in cats:
            color, r, c, d, power, stuck, stomp, status = k
            if status:
                continue
            if stuck:
                k[5] = stuck - 1
                continue
            kind, b = self.kinds[(r, c)]
            if stomp:
                k[6] = 0
                if kind == "building" and floors[b]:
                    smash_now.append(k)
                continue
            if rules.entry_mode == "stay_until_gone" and kind == "building" and floors[b]:
                smash_now.append(k)
                continue
            dr, dc = DIRS[d]
            nxt = self.kinds.get((r + dr, c + dc))
            if nxt is None or nxt[0] == "boulder" or (nxt[0] == "bed" and nxt[1] != color):
                k[3] = REVERSE[d]
                continue
            origin[color] = (r, c)
            k[1], k[2] = r + dr, c + dc
            moved.append(k)

        def fight(group):
            group.sort(key=lambda k: (-k[4], BED_RANK[k[0]]))
            for loser in group[1:]:
                if rules.fight_mode == "absorb":
                    group[0][4] += loser[4]
                loser[7] = "out"

        for i, a in enumerate(moved):  # head-on swaps
            for b in moved[i + 1:]:
                if not a[7] and not b[7] and origin[a[0]] == (b[1], b[2]) and origin[b[0]] == (a[1], a[2]):
                    fight([a, b])
        by_tile = {}
        for k in cats:
            if k[7] != "out":
                by_tile.setdefault((k[1], k[2]), []).append(k)
        for group in by_tile.values():
            if len(group) > 1:
                fight(group)

        def smash(k):
            nonlocal money
            _, b = self.kinds[(k[1], k[2])]
            fid = self.floor_id(b, floors[b])
            kind = self.buildings[b][1]
            floors[b] -= 1
            k[4] = k[4] * 2 if FLOOR_VALUE[kind] == "x2" else k[4] + FLOOR_VALUE[kind]
            cmd = choose(k[0], fid, money)
            if isinstance(cmd, tuple):  # ("paid", cmd): a command already paid for elsewhere
                cmd = cmd[1]
            elif cmd is not None:
                money -= COST[cmd]
                if money < 0:
                    return False
            if cmd in DIRS:
                k[3] = cmd
            elif cmd == "stomp":
                k[6] = 1
            return True

        arriving = []
        for k in smash_now:
            if k[7] != "out" and not smash(k):
                return None
        for k in moved:
            if k[7] == "out":
                continue
            kind, b = self.kinds[(k[1], k[2])]
            if kind == "building" and floors[b]:
                if not smash(k):
                    return None
                if rules.entry_mode == "all_on_entry":
                    while floors[b]:
                        if not smash(k):
                            return None
            elif kind == "mud":
                k[5] = 1
            elif kind == "spike":
                k[4] = k[4] / 2
            elif kind == "bed":
                arriving.append(k)
        for k in sorted(arriving, key=lambda k: k[4]):  # simultaneous: lower score enters first
            arrivals += 1
            k[7] = "bed"
            k[4] = k[4] + 2000 if arrivals == 1 else k[4] * (3 if arrivals == 2 else 5)

        return (turn + 1, tuple(tuple(k) for k in cats), tuple(floors), arrivals, money)

    @staticmethod
    def score(state):
        return sum(k[4] for k in state[1] if k[7] != "out")


def simulate(plan=None, rules: Rules = Rules(), board=BOARD, trace=None):
    """Run a fixed plan {(r, c, floor_index_from_top): command}. Returns (score, final_state)."""
    plan = plan or {}
    game = Game(board, rules)
    if sum(COST[v] for v in plan.values()) > rules.budget:
        raise ValueError("plan exceeds budget")
    state = game.initial
    for _ in range(rules.turns):
        state = game.step(state, lambda color, fid, money: plan.get(fid))
        if trace is not None:
            trace.append(state)
    return Game.score(state), state
