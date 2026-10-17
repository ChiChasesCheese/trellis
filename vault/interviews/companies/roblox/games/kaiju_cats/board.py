"""Kaiju Cats maps, transcribed tile by tile from Chi's screenshots.

Coordinates are (row, col), row 0 at the top, col 0 at the left, as the game is shown on screen.
None = no tile there (the road outline has a notch). Render a map with render_board.py and compare it against the
screenshot before trusting anything built on it. BOARD is the map the tools use.
"""

H, L, P = "high", "low", "plant"  # 2 x 500, 2 x 250, 1 floor x2
GRASS, MUD, SPIKE, ROCK = "grass", "mud", "spike", "boulder"

# Map 1 (2026-09-27, first clean screenshot, $200).
MAP1 = [
    # c0          c1     c2     c3     c4     c5     c6
    ["start:B",  H,     L,     L,     GRASS, P,     None],       # r0
    [None,       GRASS, L,     P,     MUD,   L,     "bed:R"],    # r1
    ["start:R",  L,     SPIKE, L,     GRASS, H,     "bed:G"],    # r2
    [None,       GRASS, L,     H,     ROCK,  P,     "bed:B"],    # r3
    ["start:G",  H,     GRASS, L,     L,     H,     None],       # r4
]

# Map 2 (2026-09-27, second screenshot; Chi had 8 commands placed, $90 left — see CHI_PLAN_MAP2).
MAP2 = [
    # c0          c1     c2     c3     c4     c5     c6
    ["start:B",  L,     GRASS, H,     L,     L,     None],       # r0
    [None,       L,     GRASS, P,     ROCK,  H,     "bed:R"],    # r1
    ["start:R",  L,     H,     SPIKE, P,     GRASS, "bed:G"],    # r2
    [None,       L,     MUD,   GRASS, H,     L,     "bed:B"],    # r3
    ["start:G",  H,     L,     L,     GRASS, P,     None],       # r4
]
# Chi's own commands on the map 2 screenshot, (r, c, floor from top): command. $110, matches "$90 Available".
CHI_PLAN_MAP2 = {
    (0, 3, 1): "W", (1, 1, 0): "E", (1, 3, 0): "N", (2, 1, 0): "N",
    (2, 2, 0): "stomp", (2, 2, 1): "E", (2, 4, 0): "powerup", (4, 2, 0): "N",
}

# Map 3 (2026-09-27, third screenshot, $200, no commands).
MAP3 = [
    # c0          c1     c2     c3     c4     c5     c6
    ["start:B",  L,     L,     H,     L,     GRASS, None],       # r0
    [None,       GRASS, MUD,   P,     H,     L,     "bed:R"],    # r1
    ["start:R",  H,     L,     GRASS, SPIKE, H,     "bed:G"],    # r2
    [None,       GRASS, P,     ROCK,  L,     L,     "bed:B"],    # r3
    ["start:G",  H,     L,     GRASS, P,     L,     None],       # r4
]

BOARD = MAP3

FLOORS = {H: [500, 500], L: [250, 250], P: ["x2"]}  # top floor first
COST = {"N": 10, "S": 10, "E": 10, "W": 10, "stomp": 20, "powerup": 30}
BUDGET = 200
TURNS = 15
