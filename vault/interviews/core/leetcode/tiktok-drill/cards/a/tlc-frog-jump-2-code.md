---
id: tlc-frog-jump-2-code
node: a.frog-jump
type: qa
step: 2
---
## Q
**LC 403 青蛙过河**｜写出 Python 实现

`stones` 是严格升序的石子位置（`2 <= len <= 2000`，`stones[0] == 0`，位置至多 `2^31 - 1`）。青蛙从位置 `0` 出发，第一步只能跳 `1`；上一步跳 `k`，下一步只能跳 `k - 1`、`k` 或 `k + 1`（必须为正），只能落在石子上。判断能否到达最后一块石子。

## A
**思路。** `jumps` 字典：石子位置 → 能以哪些「最后一跳长度」站在这块石子上。起点放入 `0`（相当于上一跳为 `0`，下一跳只有 `1` 为正）。按石子升序遍历，对集合里每个 `k`，尝试 `k − 1, k, k + 1`，落点是石子且步长为正就把步长记入落点的集合。

```python
def can_cross(stones: list[int]) -> bool:
    jumps: dict[int, set[int]] = {pos: set() for pos in stones}   # 石子位置 -> 能以哪些「最后一跳长度」站上来
    jumps[0].add(0)                            # 起点：当作上一跳长度 0，于是下一跳只能是 1
    for pos in stones:
        for k in jumps[pos]:
            for step in (k - 1, k, k + 1):
                if step > 0 and pos + step in jumps:
                    jumps[pos + step].add(step)
    return bool(jumps[stones[-1]])
```

运行：`[0,1,3,5,6,8,12,17]` → `True`，`[0,1,2,3,4,8,9,11]` → `False`，`[0,1]` → `True`，`[0,2]` → `False`，`[0,1,2]` → `True`，`[0, 2^31 - 1]` → `False`；`2000` 块连续石子约 `0.01` 秒。

**复杂度。** 时间 `O(n^2)`：第 `i` 块石子的集合大小不超过 `i + 1`，每个元素做 3 次转移；空间 `O(n^2)`。

**写法要点。** 字典推导 `{pos: set() for pos in stones}` 一次建好所有石子，同时让 `pos + step in jumps` 成为 `O(1)` 的「落点是不是石子」；`step > 0` 既满足「向前」，又避免在遍历 `jumps[pos]` 时往同一个集合里加元素（`step = 0` 会让 `pos + 0` 就是自己，触发 `Set changed size during iteration`）；遍历 `stones` 时写入的是后面的石子，当前石子的集合已经定型。
