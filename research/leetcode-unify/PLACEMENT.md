# Placing a problem on the LeetCode tree

Use this for a problem that is not on any of 0x3F's lists. The tree is `sources/local/lc/tree.json`; its leaves are the
nodes that have candidates.

1. Read the problem's body: its 一句话 and its code. Place it by the **method its main solution uses**, not by the
   story. Pick the most specific leaf whose method that is.
2. Design problems (LRU cache, design-linked-list, iterators) go to the matching data-structure or design leaf.
3. If no leaf fits well, add a leaf of ours under the closest heading. Put it in `sources/local/lc/our_leaves.json` as
   `{"<parent id>": [{"id": "<short-slug>", "title": "中文标题", "summary": "一句话：这类题的方法"}]}`. Its id becomes
   `<parent>.our-<short-slug>`. Keep these leaves few and give each 2+ problems where possible. Problems with no LeetCode
   number (company-written questions) go to a 公司自拟题 leaf of ours.
4. Append the problem to the list under the leaf id in `sources/local/lc/expand.json`:
   `{"num", "title", "slug", "rating" (0 if unknown), "members" (premium?), "importance"}`. Take `importance` from
   `sources/local/lc/analysis.json`, or use 0.
5. Run `uv run python scripts/lc_tree.py --write` and check that the stub `lct-<slug>.md` exists.
