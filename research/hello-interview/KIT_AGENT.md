# Drill agent — runnable LLD problems for the study plan

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your problems' folders. Scratch in `/tmp/kit_<group>/`. `git checkout uv.lock` whenever uv touches it.
**Resume rule:** skip a problem whose gate already passes.

Chi practises LLD by writing code under a timer, in stages, like a machine-coding round, in Python. The bank already has 59 drills; yours fill the gaps. The tracked model:
`vault/domains/low-level-design/problems/parking-lot/` and `vault/domains/low-level-design/drills/problems/design-parking-lot.md`. Read them first.

**This folder is public.** Statements, code and write-ups are entirely your own. Do not open `sources/local/hello-interview/premium/` or any card under `cards/premium/`. Tracked answers named in your group file are fine as a starting point.

## Output: `vault/interviews/core/low-level-design/problems/<slug>/`

- `problem.md`: `# <中文题名>（English name）`, a short scene, then `**分关要求**`: 第 1 关（约 N 分钟）, 第 2 关, 第 3 关, 第 4 关（选做）. Levels 1–3 sum to at most 60 minutes. Level 1 is a working core of about 90 lines of solution code. Each later level is the kind of change an interviewer adds and must
  not require rewriting what passed. State the exact API with types and the exact errors raised, with 2–3 concrete examples. Then `**评分点**`: 5–8 things a senior is judged on.
- `starter.py`: the same public API, bodies `raise NotImplementedError`, docstrings stating each method's contract.
- `solution.py`: standard library only, Python 3.11+, type hints, Chinese comments carrying the reasoning. Time comes from an injected clock when time matters.
- `test_<slug with underscores>.py`: at top `impl = importlib.import_module(os.environ.get("IMPL", "solution"))`. Test names start `test_part1_`, `test_part2_`, … so `-k part1` selects a level. At least 4 tests per level, covering boundary cases and the errors; deterministic; a concurrency test
  uses barriers and a small thread count, never sleeps for timing. Tests touch only the API in `problem.md`.
- `solution.md`: Chinese. `**一句话。**`, `**关键决策。**` (the decisions and why, with the rejected option), `**写法。**` (2-5 bullets: the idiom or technique, why it fits here, what the plainer alternative costs, and its general pattern as one short name), `**每关怎么走。**`, `**易错。**`, `**追问。**`, `**级别期望。**`. Refers to `solution.py`; does not restate its code.

## Gate, in each problem folder

```
IMPL=solution uv run --with pytest python -m pytest -q -p no:cacheprovider    # all pass
IMPL=starter  uv run --with pytest python -m pytest -q -p no:cacheprovider    # all fail
```

Also write a quick check that the first level alone is within about 100 lines by reading your code honestly, and run `uv run python scripts/plain_style.py <your md files>`. The style checker rejects 这道题, 本题, 本书, 抓取 and 面经.
Reply in ≤ 6 lines: problems done, tests per problem, level 1 line count, anything you changed from the tracked answer.
