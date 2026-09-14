---
id: cc-algorithms-sliding-window-covering
node: algorithms.sliding-window
type: qa
---
## Q
Shortest window of a text containing every required word, with multiplicity. Structure?

## A
**A counter of what is still needed plus a single `missing` scalar.**

```python
need = Counter(required); missing = len(required)
l, best = 0, None
for r, w in enumerate(words):
    if need[w] > 0: missing -= 1
    need[w] -= 1
    while missing == 0:                          # valid ⇒ try to shrink
        if best is None or r - l < best[1] - best[0]:
            best = (l, r)
        need[words[l]] += 1
        if need[words[l]] > 0: missing += 1
        l += 1
```

- Letting `need` go **negative** is what tracks surplus copies; clamping it at 0 breaks the shrink test.
- The scalar `missing` is why validity is O(1) to check instead of a scan over the counter.
- Ties on length resolve to the earliest window, because a later equal-length one never passes the strict `<`.
- A required word absent from the text leaves `best is None` — emit the declared sentinel, not an exception ([[cc-output-sentinels-none-vs-blank]]).

## Q zh
在一段文本中，求包含全部必需词（含重数）的最短窗口。用什么结构？

## A zh
**一个记录「还缺什么」的计数器，加一个标量 `missing`。**

```python
need = Counter(required); missing = len(required)
l, best = 0, None
for r, w in enumerate(words):
    if need[w] > 0: missing -= 1
    need[w] -= 1
    while missing == 0:                          # 合法 ⇒ 尝试收缩
        if best is None or r - l < best[1] - best[0]:
            best = (l, r)
        need[words[l]] += 1
        if need[words[l]] > 0: missing += 1
        l += 1
```

- 让 `need` 变**负**正是记录多余副本的方式；把它钳在 0 会破坏收缩判据。
- 有了标量 `missing`，合法性检查才是 O(1)，而不是扫一遍计数器。
- 长度并列时会落到最早的窗口，因为后来的等长窗口过不了严格的 `<`。
- 文本里缺少某个必需词时 `best` 仍为 `None` —— 输出约定的哨兵，而不是抛异常（[[cc-output-sentinels-none-vs-blank]]）。
