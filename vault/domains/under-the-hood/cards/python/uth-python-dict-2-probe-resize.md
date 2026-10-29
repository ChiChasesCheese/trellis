---
id: uth-python-dict-2-probe-resize
node: python.dict
type: qa
step: 2
---
## Q
**两个 key 抢同一个槽怎么办**｜Python · CPython 3.14

两个 key 落到同一个槽时，`dict` 怎么找下一个槽？表什么时候扩容？

## A
**背景。** 表只有 8 格，key 却可能很多，两个 key 算到同一格（冲突）是常事。最简单的办法是顺着往后一格一格找空位（线性探测），但被占的格子会连成一长串，越长越容易再撞上，查找变慢。

**结构。** `dict` 用开放寻址（open addressing）：不挂链表，冲突了就在表里按公式换一个槽。公式 `i = (i*5 + perturb + 1) & mask` 每次跳得很远；`perturb` 一开始是完整哈希值，每轮右移 5 位，让高位也逐步参与。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="26" y="78" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="44" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="62" y="78" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="98" y="78" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="116" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="78" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="152" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="170" y="78" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="206" y="78" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="224" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="242" y="78" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="278" y="78" width="36" height="30" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="224" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<text x="116" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2</text>
<text x="44" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k3</text>
<text x="152" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k4</text>
<text x="260" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k5</text>
<text x="296" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">new</text>
<path d="M 224 74 C 196 30 128 30 116 74" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="116.0,74.0 114.9,67.4 120.7,69.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 116 74 C 148 8 268 8 296 74" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="296.0,74.0 290.8,69.8 296.3,67.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="180" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="228" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8 槽最多放 5 个 放第 6 个就扩容</text>
<text x="170" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新表长 = 已用数 x 3 取 2 的幂</text>
</svg>
```

**细节。**

- 初始表长 8，最多用 2/3（8 槽放 5 个）；放满就按 `已用数 × 3` 向上取 2 的幂扩容。
- 实测 `getsizeof` 在放入第 1、6、11、22、43 个 key 时跳变。

**为什么。** 线性探测会让相邻哈希值挤成一团，`5*j+1` 走遍所有槽并打散聚集；留 1/3 空槽让探测很快结束。

**例题：** LC 1 两数之和

给整数数组 `nums` 和目标值 `target`，返回和为 `target` 的两个元素的下标；答案唯一，同一个元素不能用两次。例：`nums = [2,7,11,15], target = 9` 返回 `[0,1]`。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}                  # 值 -> 下标
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:   # 先查：只会匹配到前面的元素
            return [j, i]
        seen[x] = i                            # 后存：自己不会和自己配对
    return []
```
