import random

import pytest

INGREDIENTS = ["egg", "flour", "sugar", "egg", "milk", "sugar", "butter"]
RECIPES = [
    ["flour", "sugar"],
    ["sugar", "egg"],
    ["egg", "milk", "sugar"],
    ["egg", "flour", "sugar", "egg"],
    ["nope"],
]
EXPECTED = [True, True, True, True, False]


def _forbidden(*_a, **_k):
    raise AssertionError("Part 2 must not build a dict/set (O(1) auxiliary space)")


def _brute(ingredients, recipe):
    n, m = len(ingredients), len(recipe)
    if m == 0:
        return True
    for start in range(n - m + 1):
        if ingredients[start : start + m] == recipe:
            return True
    return False


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_examples_part1(impl):
    assert impl.find_recipes(INGREDIENTS, RECIPES) == EXPECTED


@pytest.mark.part1
@pytest.mark.edge
def test_empty_recipe_matches(impl):
    assert impl.find_recipes(INGREDIENTS, [[]]) == [True]
    assert impl.find_recipes([], [[]]) == [True]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_ingredients_nonempty_recipe(impl):
    assert impl.find_recipes([], [["a"]]) == [False]


@pytest.mark.part1
@pytest.mark.edge
def test_recipe_longer_than_ingredients(impl):
    assert impl.find_recipes(["a", "b"], [["a", "b", "c"]]) == [False]


@pytest.mark.part1
@pytest.mark.edge
def test_recipe_equals_whole_ingredients(impl):
    assert impl.find_recipes(INGREDIENTS, [INGREDIENTS]) == [True]


@pytest.mark.part1
@pytest.mark.edge
def test_all_same_token(impl):
    ingredients = ["a"] * 20
    assert impl.find_recipes(ingredients, [["a"] * 20, ["a"] * 21]) == [True, False]


@pytest.mark.part1
def test_agrees_with_brute_force_random(impl):
    rng = random.Random(0)
    vocab = ["a", "b", "c", "d"]
    for _ in range(300):
        ingredients = [rng.choice(vocab) for _ in range(rng.randint(0, 15))]
        recipes = [[rng.choice(vocab) for _ in range(rng.randint(0, 4))] for _ in range(rng.randint(1, 5))]
        expected = [_brute(ingredients, r) for r in recipes]
        assert impl.find_recipes(ingredients, recipes) == expected, (ingredients, recipes)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_examples_part2(impl):
    for recipe, expected in zip(RECIPES, EXPECTED):
        assert impl.find_recipes_o1_space(INGREDIENTS, recipe) is expected


@pytest.mark.part2
@pytest.mark.edge
def test_empty_recipe_o1(impl):
    assert impl.find_recipes_o1_space(INGREDIENTS, []) is True
    assert impl.find_recipes_o1_space([], []) is True


@pytest.mark.part2
@pytest.mark.edge
def test_empty_ingredients_o1(impl):
    assert impl.find_recipes_o1_space([], ["a"]) is False


@pytest.mark.part2
@pytest.mark.edge
def test_builds_no_dict_or_set(impl, monkeypatch):
    monkeypatch.setattr(impl, "dict", _forbidden, raising=False)
    monkeypatch.setattr(impl, "set", _forbidden, raising=False)
    assert impl.find_recipes_o1_space(INGREDIENTS, ["egg", "milk", "sugar"]) is True
    assert impl.find_recipes_o1_space(["a"] * 30, ["a"] * 10) is True


@pytest.mark.part2
def test_o1_agrees_with_brute_force_random(impl):
    rng = random.Random(1)
    vocab = ["a", "b", "c"]
    for _ in range(300):
        ingredients = [rng.choice(vocab) for _ in range(rng.randint(0, 15))]
        recipe = [rng.choice(vocab) for _ in range(rng.randint(0, 4))]
        assert impl.find_recipes_o1_space(ingredients, recipe) == _brute(ingredients, recipe)


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_examples_part3(impl):
    assert impl.find_recipes_trie(INGREDIENTS, RECIPES) == EXPECTED


@pytest.mark.part3
@pytest.mark.edge
def test_shared_prefix_recipes(impl):
    ingredients = ["boil", "water", "add", "salt", "boil", "water", "add", "pepper"]
    recipes = [["boil", "water", "add", "salt"], ["boil", "water", "add", "pepper"], ["boil", "water", "add", "sugar"]]
    assert impl.find_recipes_trie(ingredients, recipes) == [True, True, False]


@pytest.mark.part3
@pytest.mark.edge
def test_duplicate_recipes_both_marked(impl):
    ingredients = ["a", "b", "c"]
    recipes = [["a", "b"], ["a", "b"], ["x"]]
    assert impl.find_recipes_trie(ingredients, recipes) == [True, True, False]


@pytest.mark.part3
@pytest.mark.edge
def test_empty_recipe_trie(impl):
    assert impl.find_recipes_trie(INGREDIENTS, [[]]) == [True]


@pytest.mark.part3
def test_trie_agrees_with_part1_random(impl):
    rng = random.Random(2)
    vocab = ["a", "b", "c", "d"]
    for _ in range(300):
        ingredients = [rng.choice(vocab) for _ in range(rng.randint(0, 15))]
        recipes = [[rng.choice(vocab) for _ in range(rng.randint(0, 4))] for _ in range(rng.randint(1, 6))]
        assert impl.find_recipes_trie(ingredients, recipes) == impl.find_recipes(ingredients, recipes)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part2
@pytest.mark.perf
def test_perf_o1_space_realistic(run_script):
    rng = random.Random(0)
    n = 50_000
    vocab = [f"tok{i}" for i in range(30)]
    ingredients = [rng.choice(vocab) for _ in range(n)]
    recipe = ingredients[1000:1030]  # a real 30-token run, guaranteed to match
    body = "INGREDIENTS " + " ".join(ingredients)
    stdin = f"PART 2\n{body}\nRECIPE {' '.join(recipe)}\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "true"
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_trie_shared_prefixes(run_script):
    rng = random.Random(0)
    n = 20_000
    vocab = [f"tok{i}" for i in range(15)]
    ingredients = [rng.choice(vocab) for _ in range(n)]
    # 300 recipes sharing a common prefix
    prefix = ["shared", "prefix", "run"]
    recipes = [prefix + [f"end{i}"] for i in range(300)]
    body = "INGREDIENTS " + " ".join(ingredients)
    recipe_lines = "\n".join(" ".join(r) for r in recipes)
    stdin = f"PART 3\n{body}\nN {len(recipes)}\n{recipe_lines}\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 300
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    body = "INGREDIENTS " + " ".join(INGREDIENTS)
    r = run_script(f"PART 1\n{body}\nN 2\nflour sugar\nnope\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\nfalse\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    body = "INGREDIENTS " + " ".join(INGREDIENTS)
    r = run_script(f"PART 2\n{body}\nRECIPE egg milk sugar\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    body = "INGREDIENTS " + " ".join(INGREDIENTS)
    r = run_script(f"PART 3\n{body}\nN 2\nflour sugar\nnope\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\nfalse\n"
