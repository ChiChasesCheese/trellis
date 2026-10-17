"""Render board.py to board.png so the model can be checked against the game screenshot, tile by tile.
With a plan file, also draw each command on its floor and each cat's path, and write <plan>.png.

    uv run --no-project --with matplotlib python3 render_board.py [plan_stay.json]
"""
import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from board import BOARD, FLOORS, GRASS, MUD, SPIKE, ROCK, H, L, P

CAT = {"R": "#d33a2c", "G": "#3dbf8a", "B": "#2f6fd6"}
STYLE = {
    H: ("#f2d774", "HIGH\n2 floors\n500 + 500"),
    L: ("#e6e6ea", "LOW\n2 floors\n250 + 250"),
    P: ("#9b59d0", "POWER PLANT\n1 floor\nx2"),
    GRASS: ("#8fd18a", "grass"),
    MUD: ("#8a5a32", "MUD\nstuck 1 turn"),
    SPIKE: ("#555566", "SPIKE\npower / 2"),
    ROCK: ("#9a9a9a", "BOULDER\nrebound"),
}

fig, ax = plt.subplots(figsize=(14, 10))
rows, cols = len(BOARD), len(BOARD[0])
for r, row in enumerate(BOARD):
    for c, cell in enumerate(row):
        x, y = c, rows - 1 - r
        if cell is None:
            ax.text(x + 0.5, y + 0.5, "(no tile)", ha="center", va="center", color="#bbbbbb", fontsize=9)
            continue
        if cell.startswith("start:"):
            color, label, fg = CAT[cell[-1]], f"{cell[-1]} cat start\n(grass)", "white"
        elif cell.startswith("bed:"):
            color, label, fg = CAT[cell[-1]], f"{cell[-1]} BED\nonly {cell[-1]} enters", "white"
        else:
            color, label = STYLE[cell]
            fg = "white" if cell in (P, MUD, SPIKE) else "black"
        ax.add_patch(FancyBboxPatch((x + 0.06, y + 0.06), 0.88, 0.88, boxstyle="round,pad=0.02", fc=color, ec="#333"))
        ax.text(x + 0.5, y + 0.5, label, ha="center", va="center", fontsize=10, color=fg, fontweight="bold")
        ax.text(x + 0.1, y + 0.86, f"r{r}c{c}", fontsize=8, color=fg)
out, title = "board.png", "Kaiju Cats practice level — model in board.py (row 0 on top)"
if len(sys.argv) > 1:
    from sim import Rules, simulate

    data = json.load(open(sys.argv[1]))
    plan = {tuple(x[:3]): x[3] for x in data["plan"]}
    rules = Rules(rebound=data["rules"]["rebound"], powerup_first=data["rules"]["powerup_first"])
    score, _, log = simulate(plan, rules)
    ARROW = {"N": "↑", "S": "↓", "E": "→", "W": "←", "stomp": "STOMP", "powerup": "+1000"}
    for (r, c, i), cmd in plan.items():
        x, y = c, rows - 1 - r
        ax.text(x + 0.5, y + (0.22 if i else 0.08) + 0.04, f"{'bottom' if i else 'top'}: {ARROW[cmd]}",
                ha="center", fontsize=11, color="#b00020", fontweight="bold",
                bbox=dict(fc="white", ec="#b00020", pad=1.5))
    # paths from the trace lines "    X at rRcC ..."
    paths = {k: [] for k in CAT}
    for line in log:
        parts = line.split()
        if len(parts) > 2 and parts[1] == "at":
            rc = parts[2][1:].split("c")
            paths[parts[0]].append((int(rc[0]), int(rc[1])))
    offset = {"R": -0.12, "G": 0.0, "B": 0.12}
    from board import BOARD as _B
    for color, pts in paths.items():
        start = next((r, c) for r, row in enumerate(_B) for c, v in enumerate(row) if v == f"start:{color}")
        pts = [start] + pts
        xs = [c + 0.5 + offset[color] for r, c in pts]
        ys = [rows - 1 - r + 0.5 + offset[color] for r, c in pts]
        ax.plot(xs, ys, "-", color=CAT[color], lw=3, alpha=0.8)
        for t, (xx, yy) in enumerate(zip(xs, ys)):
            if t and (xx, yy) != (xs[t - 1], ys[t - 1]):
                ax.text(xx, yy, str(t), fontsize=8, color="white", ha="center", va="center",
                        bbox=dict(boxstyle="circle,pad=0.15", fc=CAT[color], ec="none"))
    out = sys.argv[1].replace(".json", ".png")
    title = f"{sys.argv[1].rsplit("/", 1)[-1]}: score {score:g}, cost ${data['cost']}  (numbers = turn the cat arrives)"
ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title(title, fontsize=13)
fig.savefig(out, dpi=110, bbox_inches="tight")
print(out, "written")
