"""Kaiju Cats simulator on the map in board.py.

Every rule below is tagged with where it comes from:
  [game]  the in-game instructions (screenshots 2026-09-27)
  [Chi]   Chi's answers, 2026-09-27
  [open]  not stated anywhere yet; a switch in Rules, to be settled by an in-game calibration run

Turn, all three cats at once:
  1. each active cat decides: stuck in mud -> stays; stomping -> stays; else moves one tile in its direction.
     A blocked move (no tile, off the board, boulder, another cat's bed) reverses the cat's direction  [game+Chi]
     and stays on its own tile this turn  [Chi, seen in game 2026-09-27; Rules.rebound="step" kept only for comparison]
  2. fights: cats that end on one tile, or swap tiles head-on, fight; higher power wins, a tie goes to the
     topmost bed (R > G > B); losers die and score 0  [game+Chi]
  3. effects on the tile each survivor entered (or stomps in):
     building with floors left -> destroys ONE floor (the top one), gains its value, fires its command;
       next turn the cat moves on in its direction  [Chi]
     mud -> stuck next turn, then continues  [game]; spike -> power halved  [game]; bed -> enters, stops  [game]
  4. cats entering beds the same turn go in lowest power first; bed #1 +2000, #2 x3, #3 x5  [game]
Commands fire when their floor is destroyed, whoever destroys it  [Chi]:
  turn N/S/E/W sets the direction; stomp: the cat stays next turn and destroys the next floor  [game]
  powerup: +1000  [game]; on a power plant floor, Rules.powerup_first decides x2 vs +1000 order  [open]
Cats start with 0 power facing east  [Chi]. Score = total power of every cat still alive after 15 turns, in a bed
or not  [Chi, corrected 2026-09-27: a cat outside its bed still counts; only a dead cat scores 0].
"""
from __future__ import annotations

from dataclasses import dataclass

from board import BOARD, BUDGET, COST, FLOORS, GRASS, MUD, P, ROCK, SPIKE, TURNS

DIRS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
REVERSE = {"N": "S", "S": "N", "E": "W", "W": "E"}
BED_RANK = {"R": 0, "G": 1, "B": 2}  # topmost bed wins a tie
COLORS = ("R", "G", "B")


@dataclass(frozen=True)
class Rules:
    rebound: str = "stay"  # [open] "stay": a blocked cat turns around in place | "step": it also moves back one tile
    powerup_first: bool = False  # [open] on a power plant floor: +1000 then x2 (True) or x2 then +1000 (False)
    turns: int = TURNS
    budget: int = BUDGET


def parse(board=BOARD):
    tiles, starts, beds, buildings = {}, {}, {}, []
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell is None:
                continue
            if cell.startswith("start:"):
                starts[cell[-1]] = (r, c)
                tiles[(r, c)] = (GRASS, None)
            elif cell.startswith("bed:"):
                beds[(r, c)] = cell[-1]
                tiles[(r, c)] = ("bed", cell[-1])
            elif cell in FLOORS:
                tiles[(r, c)] = ("building", len(buildings))
                buildings.append(((r, c), cell))
            else:
                tiles[(r, c)] = (cell, None)
    return tiles, starts, buildings


# cat = (color, r, c, dir, power, mode, alive, bedded)
#   mode: "" moving | "mud" stuck next turn | "stomp" stays next turn and destroys the next floor
# state = (turn, cats, floors_left per building, beds_filled, money)
class Game:
    def __init__(self, board=BOARD, rules: Rules = Rules(), colors=COLORS):
        self.rules = rules
        self.tiles, starts, self.buildings = parse(board)
        cats = tuple((col, *starts[col], "E", 0, "", True, False) for col in colors)
        self.initial = (0, cats, tuple(len(FLOORS[k]) for _, k in self.buildings), 0, rules.budget)

    def floor_id(self, b, left):
        """(r, c, i): floor i of the building at (r, c), 0 = top floor."""
        (r, c), kind = self.buildings[b]
        return (r, c, len(FLOORS[kind]) - left)

    def blocked(self, color, pos):
        t = self.tiles.get(pos)
        return t is None or t[0] == ROCK or (t[0] == "bed" and t[1] != color)

    def step(self, state, choose, log=None):
        """One turn. choose(color, floor_id, money) -> command or None for a floor being destroyed now; each floor is
        destroyed once, so choosing at destruction time is the same as fixing a plan up front. None if over budget."""
        turn, cats, floors, filled, money = state
        cats = [list(k) for k in cats]
        floors = list(floors)
        origin, acting = {}, []  # acting: cats that entered a tile, or stomp in place, this turn

        for k in cats:
            color, r, c, d, power, mode, alive, bedded = k
            if not alive or bedded:
                continue
            origin[color] = (r, c)
            if mode == "mud":
                k[5] = ""
                continue
            if mode == "stomp":
                k[5] = ""
                acting.append(k)
                continue
            dr, dc = DIRS[d]
            if self.blocked(color, (r + dr, c + dc)):
                k[3] = d = REVERSE[d]
                if self.rules.rebound == "stay":
                    continue
                dr, dc = DIRS[d]
                if self.blocked(color, (r + dr, c + dc)):
                    continue
            k[1], k[2] = r + dr, c + dc
            acting.append(k)

        def fight(group):
            group.sort(key=lambda k: (-k[4], BED_RANK[k[0]]))
            for loser in group[1:]:
                loser[6], loser[4] = False, 0
                if log is not None:
                    log.append(f"  {loser[0]} loses a fight to {group[0][0]} at {tuple(loser[1:3])}")

        live = [k for k in cats if k[6] and not k[7]]
        for i, a in enumerate(live):  # head-on swaps
            for b in live[i + 1:]:
                if a[6] and b[6] and origin[a[0]] == (b[1], b[2]) and origin[b[0]] == (a[1], a[2]) \
                        and origin[a[0]] != origin[b[0]]:
                    fight([a, b])
        by_tile = {}
        for k in cats:
            if k[6]:
                by_tile.setdefault((k[1], k[2]), []).append(k)
        for group in by_tile.values():
            if len(group) > 1:
                fight(group)

        arriving = []
        for k in acting:
            if not k[6]:
                continue
            kind, b = self.tiles[(k[1], k[2])]
            if kind == "building":
                if floors[b] == 0:
                    continue  # rubble: plain ground [Chi]
                fid = self.floor_id(b, floors[b])
                floors[b] -= 1
                cmd = choose(k[0], fid, money)
                if isinstance(cmd, tuple):  # ("paid", cmd): attached up front, already paid for
                    cmd = cmd[1]
                elif cmd is not None:
                    money -= COST[cmd]
                    if money < 0:
                        return None
                value = FLOORS[self.buildings[b][1]][fid[2]]
                if cmd == "powerup" and self.rules.powerup_first:
                    k[4] += 1000
                k[4] = k[4] * 2 if value == "x2" else k[4] + value
                if cmd == "powerup" and not self.rules.powerup_first:
                    k[4] += 1000
                if cmd in DIRS:
                    k[3] = cmd
                elif cmd == "stomp":
                    k[5] = "stomp"
                if log is not None:
                    log.append(f"  {k[0]} destroys {fid} ({value}){' +' + cmd if cmd else ''} -> {k[4]:g}")
            elif kind == MUD:
                k[5] = "mud"
            elif kind == SPIKE:
                k[4] = k[4] / 2
            elif kind == "bed":
                arriving.append(k)
        for k in sorted(arriving, key=lambda k: k[4]):
            filled += 1
            k[7] = True
            k[4] = k[4] + 2000 if filled == 1 else k[4] * (3 if filled == 2 else 5)
            if log is not None:
                log.append(f"  {k[0]} enters its bed #{filled} -> {k[4]:g}")
        return (turn + 1, tuple(tuple(k) for k in cats), tuple(floors), filled, money)

    @staticmethod
    def score(state):
        return sum(k[4] for k in state[1] if k[6])


def simulate(plan=None, rules: Rules = Rules(), board=BOARD, verbose=False):
    """Run a plan {(r, c, floor_index_from_top): command}. Returns (score, final_state, log lines)."""
    plan = plan or {}
    if sum(COST[v] for v in plan.values()) > rules.budget:
        raise ValueError("plan exceeds budget")
    game = Game(board, rules)
    state, log = game.initial, []
    # in the game every attached command is paid for up front, whether a cat ever destroys its floor or not
    state = state[:4] + (rules.budget - sum(COST[v] for v in plan.values()),)
    for t in range(rules.turns):
        log.append(f"turn {t + 1}")
        state = game.step(state, lambda color, fid, money: ("paid", plan[fid]) if fid in plan else None, log)
        for k in state[1]:
            status = "dead" if not k[6] else "bed" if k[7] else k[5] or "ok"
            log.append(f"    {k[0]} at r{k[1]}c{k[2]} facing {k[3]} power {k[4]:g} {status}")
    if verbose:
        print("\n".join(log))
    return Game.score(state), state, log


if __name__ == "__main__":
    s, _, _ = simulate(verbose=True)
    print("score with no commands:", s)
