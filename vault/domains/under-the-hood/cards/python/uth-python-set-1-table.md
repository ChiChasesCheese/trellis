---
id: uth-python-set-1-table
node: python.set
type: qa
step: 1
---
## Q
**set 怎么做到秒判断「在不在」**｜Python · CPython 3.14

`x in s` 为什么比 `list` 快得多？`set` 的内部结构和 `dict` 有什么不同，什么时候扩容？

## A
**背景。** 只关心「在不在」（去重、判断成员）时，`list` 要从头逐个比，O(n)。`set` 用的是和 `dict` 同一个思路：用哈希值直接算出该去哪一格看，但不需要存 value。

**结构。** 直接存条目的开放寻址表（冲突了在表里另找空位），条目只有 `key` 和缓存的 `hash`，没有 value，也没有 `dict` 的索引数组。例：8 格的表依次放 3、8、11，3 去第 3 格，8 去第 0 格，11 也算到第 3 格，被占了，就在相邻格里线性往后找，落在第 4 格。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8 格的表 依次放 3 8 11</text>
<rect x="26" y="56" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="44" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="44" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="62" y="56" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="98" y="56" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="56" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="152" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="152" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="170" y="56" width="36" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="188" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<text x="188" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="206" y="56" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="224" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="242" y="56" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="278" y="56" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="44" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8&amp;7</text>
<text x="152" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3&amp;7</text>
<line x1="164" y1="124" x2="182" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="182.0,124.0 176.0,127.0 176.0,121.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">11&amp;7 也是 3 被占了 顺延到 4</text>
</svg>
```

**细节。**

- 初始 8 槽；填充超过约 3/5（`fill*5 >= mask*3`）就扩容，新表按元素数的 4 倍（超过 5 万个则 2 倍）。
- 探测先在相邻的 9 个槽里线性找，再跳到别处。
- 实测第 5 个元素放入时 `getsizeof` 从 216 跳到 728。

**为什么。** `set` 主要做成员判断，不存在的 key 占多数，所以要缓存友好的短探测；不要求保序，就省掉索引层。

**例题：** LC 217 存在重复元素

给整数数组 `nums`，判断是否有某个值至少出现两次，有返回 `true`，否则返回 `false`。`1 <= nums.length <= 10^5`。

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```
