"""pc27 Recipe Sequence Matcher -- reference solution.

`ingredients` is a list of tokens; each `recipe` is a list of tokens; a recipe "appears" iff it
occurs as a CONTIGUOUS run inside `ingredients` (an exact-substring-of-a-sequence problem, not a
subsequence problem).

Part1: preprocessing over `ingredients` is allowed -- we build a hash of positions (a map from
each token to the sorted list of indices where it occurs) and, for the rare-first-token
optimisation, verify candidates directly; this is simple, correct, and fast enough, and doubles
as the reference oracle other parts are checked against. (KMP / rolling hash would give the same
answer in the same asymptotic class; problem.md discusses the tradeoff.)

Part2 (reconstructed follow-up, stated in the source preview): match with O(1) AUXILIARY memory
(no hash of positions, no per-recipe automaton) -- a two-pointer restart scan, à la the naive
substring-search algorithm.

Part3 (reconstructed): many recipes sharing prefixes -- build a trie of all recipes and walk
`ingredients` once, advancing/branching over the trie's nodes, so shared prefixes are compared
once instead of once per recipe.
"""

from __future__ import annotations

import sys
from collections import defaultdict

# --------------------------------------------------------------------------- Part 1
def find_recipes(ingredients: list[str], recipes: list[list[str]]) -> list[bool]:
    """For each recipe, whether it appears as a contiguous run in `ingredients`. Preprocessing
    over `ingredients` allowed: index positions by token, then for each recipe only check the
    (rare) positions where its first token occurs."""
    positions: dict[str, list[int]] = defaultdict(list)
    for i, tok in enumerate(ingredients):
        positions[tok].append(i)
    n = len(ingredients)

    def _matches_at(start: int, recipe: list[str]) -> bool:
        if start + len(recipe) > n:
            return False
        return all(ingredients[start + j] == recipe[j] for j in range(1, len(recipe)))

    out = []
    for recipe in recipes:
        if not recipe:
            out.append(True)  # an empty recipe trivially "occurs" (matches pc convention: state it)
            continue
        candidates = positions.get(recipe[0], [])
        out.append(any(_matches_at(p, recipe) for p in candidates))
    return out


# --------------------------------------------------------------------------- Part 2
def find_recipes_o1_space(ingredients: list[str], recipe: list[str]) -> bool:
    """Part2 (reconstructed follow-up from the source preview): single recipe, O(1) AUXILIARY
    space -- no position index, no automaton, just a two-pointer restart scan (the naive
    substring-search algorithm): at each start position in `ingredients`, compare token-by-token
    and bail out on the first mismatch. Worst case O(n*m) (n=len(ingredients), m=len(recipe)),
    e.g. ingredients = ["a"]*n, recipe = ["a"]*(m-1) + ["b"] -- but no memory beyond a couple of
    indices, unlike Part1's position index or a KMP failure table."""
    n, m = len(ingredients), len(recipe)
    if m == 0:
        return True
    for start in range(0, n - m + 1):
        i = 0
        while i < m and ingredients[start + i] == recipe[i]:
            i += 1
        if i == m:
            return True
    return False


# --------------------------------------------------------------------------- Part 3
class _TrieNode:
    __slots__ = ("children",)

    def __init__(self) -> None:
        self.children: dict[str, "_TrieNode"] = {}


def find_recipes_trie(ingredients: list[str], recipes: list[list[str]]) -> list[bool]:
    """Part3 (reconstructed): many recipes sharing prefixes. Build a trie over all recipes, then
    for each starting position in `ingredients` walk the trie one token at a time; whenever a
    trie node marked as a recipe's end is reached, that recipe is found. Shared prefixes across
    recipes are walked once per (start position) instead of once per (start position, recipe)."""
    # Build the trie once, over all (non-empty) recipes. A trie node can be the shared end of
    # several identical recipes, so each node records every recipe index that ends there.
    root = _TrieNode()
    end_indices: dict[int, list[int]] = defaultdict(list)  # id(node) -> [recipe indices]
    for idx, recipe in enumerate(recipes):
        if not recipe:
            continue  # an empty recipe trivially "occurs"; handled below, not via the trie
        node = root
        for tok in recipe:
            node = node.children.setdefault(tok, _TrieNode())
        end_indices[id(node)].append(idx)

    found = [not recipe for recipe in recipes]  # empty recipes trivially found
    n = len(ingredients)
    for start in range(n):
        node = root
        pos = start
        while pos < n and ingredients[pos] in node.children:
            node = node.children[ingredients[pos]]
            pos += 1
            if id(node) in end_indices:
                for idx in end_indices[id(node)]:
                    found[idx] = True
    return found


# --------------------------------------------------------------------------- line-driven wrappers
def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def _tok(line: str) -> list[str]:
    return line.split() if line.strip() else []


def part1(lines: list[str]) -> list[str]:
    """'INGREDIENTS <tokens...>' / 'N n' / n recipe lines -> n lines 'true'/'false'."""
    header = lines[0].split()
    if header[0] != "INGREDIENTS":
        raise ValueError(f"expected 'INGREDIENTS ...', got {lines[0]!r}")
    ingredients = header[1:]
    recipe_lines, _ = _read_n_lines(lines, 1)
    recipes = [_tok(l) for l in recipe_lines]
    return ["true" if r else "false" for r in find_recipes(ingredients, recipes)]


def part2(lines: list[str]) -> list[str]:
    """'INGREDIENTS <tokens...>' / 'RECIPE <tokens...>' -> one line 'true'/'false'."""
    header = lines[0].split()
    if header[0] != "INGREDIENTS":
        raise ValueError(f"expected 'INGREDIENTS ...', got {lines[0]!r}")
    ingredients = header[1:]
    r_header = lines[1].split()
    if r_header[0] != "RECIPE":
        raise ValueError(f"expected 'RECIPE ...', got {lines[1]!r}")
    recipe = r_header[1:]
    return ["true" if find_recipes_o1_space(ingredients, recipe) else "false"]


def part3(lines: list[str]) -> list[str]:
    """'INGREDIENTS <tokens...>' / 'N n' / n recipe lines -> n lines 'true'/'false'."""
    header = lines[0].split()
    if header[0] != "INGREDIENTS":
        raise ValueError(f"expected 'INGREDIENTS ...', got {lines[0]!r}")
    ingredients = header[1:]
    recipe_lines, _ = _read_n_lines(lines, 1)
    recipes = [_tok(l) for l in recipe_lines]
    return ["true" if r else "false" for r in find_recipes_trie(ingredients, recipes)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
