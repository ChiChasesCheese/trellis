---
id: uth-storage-query-exec-1-hash-join
node: storage.query-exec
type: qa
step: 1
---
## Q
**哈希连接 = 两数之和**｜PostgreSQL · 18

`orders JOIN users ON orders.uid = users.id` 没有合适索引时，PostgreSQL 怎么连接？表大到内存放不下呢？

## A
**背景。** 连接（join）是把两张表里“键相等”的行配成对。最直接的做法是嵌套循环：对 orders 的每一行，把 users 整张表扫一遍找配对；两张表各有 n、m 行，就要比 n × m 次。

**结构。** 哈希连接（hash join）：先扫较小的那张表（内表），把每一行按连接键放进内存里的哈希表；再逐行扫另一张表，用它的键去哈希表里查（探测，probe），一次 O(1)。总共 O(n + m)。这和两数之和是同一招：先把见过的值记进哈希表，再用 `target - x` 去查。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 142">
<rect x="8" y="34" width="76" height="60" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内表</text>
<text x="46" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(较小)</text>
<line x1="84" y1="64" x2="120" y2="64" stroke="currentColor" stroke-width="1.2"/>
<polygon points="126,64 120.0,67.0 120.0,61.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="105" y="56" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">建表</text>
<rect x="128" y="18" width="96" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="176" y="33.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0: u3 u9</text>
<rect x="128" y="44" width="96" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="176" y="59.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1: u8</text>
<rect x="128" y="70" width="96" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="176" y="85.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2: u5</text>
<rect x="128" y="96" width="96" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="176" y="111.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3:</text>
<rect x="256" y="34" width="76" height="60" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">外表</text>
<text x="294" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐行探测</text>
<line x1="256" y1="81" x2="232" y2="81" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="226,81 232.0,78.0 232.0,84.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">放不下就分批, 批数是 2 的幂</text>
</svg>
```

**细节。**

- 内存上限 = `work_mem`（默认 4 MB）× `hash_mem_multiplier`（15 起默认 2.0，14 及之前 1.0），即默认 8 MB。
- 放不下就分批（batch）：两张表按哈希值分到临时文件，一批一批地连。批数总是 2 的幂，发现某批太大就翻倍。

**为什么。** 复杂度 O(n + m)，嵌套循环是 O(n × m)；代价是只能做等值连接。

**例题：** LC 1 两数之和

给整数数组 `nums` 和 `target`，返回和为 `target` 的两个元素的下标，同一个元素不能用两次，答案唯一。例：`nums = [2,7,11,15]`，`target = 9` → `[0,1]`。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}                  # 值 -> 下标
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:   # 先查：只会匹配到前面的元素
            return [j, i]
        seen[x] = i                            # 后存：自己不会和自己配对
    return []
```
