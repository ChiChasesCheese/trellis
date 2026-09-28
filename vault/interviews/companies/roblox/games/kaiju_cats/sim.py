"""Kaiju Cats (Roblox's official practice assessment game) — a simulator built from the in-game instructions.

Rules the instructions state are implemented as written. Rules they do not state are naive assumptions, each one named
in ASSUMPTIONS below and switchable through `Rules`, so a result can be re-run under a different reading.
"""
from __future__ import annotations

from dataclasses import dataclass, field

DIRS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
REVERSE = {"N": "S", "S": "N", "E": "W", "W": "E"}
BED_RANK = {"R": 0, "G": 1, "B": 2}  # top bed beats middle beats bottom (stated tie-break in fights)

ASSUMPTIONS = """
A1 Cats start with 0 power (the beds show 0 before any test) and face east.
A2 Each turn every cat acts once, all at the same time: it moves one tile, or stays if stuck or still smashing.
A3 Entering a building destroys its top floor that turn; the cat stays on the tile and destroys one more floor per
   turn until the building is gone, then moves on (entry_mode="one_floor_per_turn"). Alternative: "all_on_entry".
A4 A floor's command fires when that floor is destroyed and sets the cat's direction.
A5 Walls, missing tiles, a boulder and another cat's bed block: the cat stays this turn and reverses direction.
A6 Two cats on one tile fight; the loser is out and its power is lost (fight_mode="eliminate"). Alternative: "absorb".
A7 Commands are the four direction arrows at $50 each, so $200 buys 4 (cost_per_command).
A8 Commands already on the board are part of the level and free; the paw command has no effect.
A9 After 15 turns the score is the sum of the powers of the cats still in play, in a bed or not.
"""


@dataclass
class Rules:
    entry_mode: str = "one_floor_per_turn"  # or "all_on_entry"
    fight_mode: str = "eliminate"  # or "absorb"
    turns: int = 15
    budget: int = 200
    cost_per_command: int = 50


@dataclass
class Cat:
    color: str  # "R" | "G" | "B"
    r: int
    c: int
    d: str = "E"
    power: float = 0
    stuck: int = 0
    in_bed: bool = False
    out: bool = False


# Board legend. Buildings: H = high value (2 x 500), L = low value (2 x 250), P = power plant (1 floor, x2).
# A building cell may carry commands per floor, top floor first, e.g. ("L", None, "E") = bottom floor points east.
# Read off the photo on 2026-09-28; floor positions of the pre-placed icons are a best reading of a slanted shot.
BOARD = [
    # c0        c1      c2                 c3        c4                 c5                  c6
    ["startB", ("L",), ("L", None, "E"),  ("H",),   ("L", None, "paw"), "grass",            None],
    [None,     "grass", "mud",             ("P",),   ("H",),            ("L",),             "bedR"],
    ["startR", ("H",), ("L", "N", None),   "grass",  "spike",           ("H", "E", None),   "bedG"],
    [None,     "grass", ("P",),            "boulder", ("L",),           ("L",),             "bedB"],
    ["startG", ("H",), ("L",),             "grass",  ("P",),            ("L", "rev", "N"),  None],
]

FLOOR_VALUE = {"H": 500, "L": 250, "P": "x2"}
FLOORS = {"H": 2, "L": 2, "P": 1}


@dataclass
class Tile:
    kind: str  # grass | mud | spike | boulder | bed | building | rubble
    bed: str | None = None
    floors: list = field(default_factory=list)  # [(value, command)], top floor first


def build_board(board=BOARD):
    tiles, starts = {}, {}
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell is None:
                continue
            if isinstance(cell, tuple):
                kind, cmds = cell[0], list(cell[1:]) + [None] * FLOORS[cell[0]]
                tiles[(r, c)] = Tile("building", floors=[[FLOOR_VALUE[kind], cmds[i]] for i in range(FLOORS[kind])])
            elif cell.startswith("start"):
                tiles[(r, c)] = Tile("grass")
                starts[cell[-1]] = (r, c)
            elif cell.startswith("bed"):
                tiles[(r, c)] = Tile("bed", bed=cell[-1])
            else:
                tiles[(r, c)] = Tile(cell)
    return tiles, starts


def simulate(plan: dict | None = None, rules: Rules = Rules(), board=BOARD, trace: list | None = None):
    """plan maps (r, c, floor_index_from_top) -> "N"|"S"|"E"|"W". Returns (score, cats, destroyed_floor_events)."""
    plan = plan or {}
    tiles, starts = build_board(board)
    for (r, c, i), d in plan.items():
        tiles[(r, c)].floors[i][1] = d
    cats = [Cat(col, *starts[col]) for col in ("R", "G", "B")]
    arrivals = 0
    events = []  # (turn, cat_color, r, c, floor_index) for every destroyed floor, in order

    def smash(cat, tile, turn):
        idx = FLOORS_TOTAL[(cat.r, cat.c)] - len(tile.floors)
        value, cmd = tile.floors.pop(0)
        cat.power = cat.power * 2 if value == "x2" else cat.power + value
        events.append((turn, cat.color, cat.r, cat.c, idx))
        if cmd in DIRS:
            cat.d = cmd
        elif cmd == "rev":
            cat.d = REVERSE[cat.d]
        if not tile.floors:
            tile.kind = "rubble"

    FLOORS_TOTAL = {pos: len(t.floors) for pos, t in tiles.items() if t.kind == "building"}

    for turn in range(1, rules.turns + 1):
        moved = []  # cats that entered a new tile this turn
        for cat in cats:
            if cat.out or cat.in_bed:
                continue
            here = tiles[(cat.r, cat.c)]
            if cat.stuck:
                cat.stuck -= 1
                continue
            if here.kind == "building" and here.floors and rules.entry_mode == "one_floor_per_turn":
                smash(cat, here, turn)
                continue
            dr, dc = DIRS[cat.d]
            nxt = tiles.get((cat.r + dr, cat.c + dc))
            if nxt is None or nxt.kind == "boulder" or (nxt.kind == "bed" and nxt.bed != cat.color):
                cat.d = REVERSE[cat.d]
                continue
            cat.r, cat.c = cat.r + dr, cat.c + dc
            moved.append(cat)

        # Fights: any tile holding two or more cats in play.
        by_tile = {}
        for cat in cats:
            if not cat.out:
                by_tile.setdefault((cat.r, cat.c), []).append(cat)
        for group in by_tile.values():
            if len(group) < 2:
                continue
            group.sort(key=lambda k: (-k.power, BED_RANK[k.color]))
            winner = group[0]
            for loser in group[1:]:
                if rules.fight_mode == "absorb":
                    winner.power += loser.power
                loser.out = True

        # Tile effects for cats that entered a tile this turn and are still in play.
        arriving = []
        for cat in moved:
            if cat.out:
                continue
            tile = tiles[(cat.r, cat.c)]
            if tile.kind == "building":
                smash(cat, tile, turn)
                if rules.entry_mode == "all_on_entry":
                    while tile.kind == "building":
                        smash(cat, tile, turn)
            elif tile.kind == "mud":
                cat.stuck = 1
            elif tile.kind == "spike":
                cat.power /= 2
            elif tile.kind == "bed":
                arriving.append(cat)
        for cat in sorted(arriving, key=lambda k: k.power):  # simultaneous: lower score enters first
            arrivals += 1
            cat.in_bed = True
            cat.power = cat.power + 2000 if arrivals == 1 else cat.power * (3 if arrivals == 2 else 5)

        if trace is not None:
            trace.append((turn, [(k.color, k.r, k.c, k.d, k.power, "bed" if k.in_bed else "out" if k.out else "")
                                 for k in cats]))

    score = sum(k.power for k in cats if not k.out)
    return score, cats, events
