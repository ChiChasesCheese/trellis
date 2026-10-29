---
id: uth-kafka-log-index-1-sparse-index
node: kafka.log-index
type: qa
step: 1
---
## Q
**按偏移量找消息：稀疏索引**｜Kafka · 4.0

一个分区的日志切成很多 1 GiB 的段（segment，日志切成的一个个文件）。消费者要从偏移量（消息序号）`N` 开始读，Kafka 怎么快速定位？索引是每条消息记一项吗？

## A
**背景。** 要在 1 GiB 的文件里找第 N 条消息：从头顺序扫太慢；给每条消息都建一项索引又太大，按每条 100 字节算，一个段要约 82 MiB 的索引。

**结构。** 稀疏索引（sparse index）：每追加超过 `index.interval.bytes`（默认 4096）字节，才记一项（4 字节相对偏移 + 4 字节文件位置）。找 N 分两步：先在索引里二分（每次砍掉一半）找出不大于 N 的最后一项，再从它指的文件位置顺序扫，只需扫不到 4 KB。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">段按首条偏移排序 (跳表 floorEntry)</text>
<rect x="8" y="20" width="96" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">段 0</text>
<rect x="112" y="20" width="96" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">段 368</text>
<rect x="216" y="20" width="96" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="264" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">段 735</text>
<line x1="264" y1="48" x2="264" y2="60" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="264,66 261.0,60.0 267.0,60.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">.index 稀疏索引: 偏移 -&gt; 文件位置</text>
<rect x="18" y="86" width="60" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="102.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">735</text>
<line x1="48" y1="110" x2="48" y2="142" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="98" y="86" width="60" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="102.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">770</text>
<line x1="128" y1="110" x2="128" y2="142" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="178" y="86" width="60" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208" y="102.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">802</text>
<line x1="208" y1="110" x2="208" y2="142" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="258" y="86" width="60" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="288" y="102.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">840</text>
<line x1="288" y1="110" x2="288" y2="142" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">.log</text>
<rect x="40" y="142" width="292" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="128" y="142" width="52" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154" y="157.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">顺序扫</text>
<line x1="180" y1="184" x2="180" y2="172" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,166 183.0,172.0 177.0,172.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">N=800</text>
</svg>
```

**细节。**

- 每段有 `.log`（消息）和 `.index`（索引）两个文件，文件名是该段首条消息偏移量（20 位，前面补 0）。
- 所有段放进一个有序表（`ConcurrentSkipListMap`），`floorEntry(N)` 取出“起点不大于 N 的最后一段”。

**为什么。** 1 GiB 的段只要 262144 项、2 MiB 的索引，能整个映射进内存（mmap）；逐条建索引多花的内存，换来的只是少扫不到 4 KB。

**例题：** LC 34 在排序数组中查找元素的第一个和最后一个位置

给非递减数组 `nums` 和目标值 `target`，返回 `target` 的起止下标，不存在返回 `[-1, -1]`，要求 O(log n)。例：`nums = [5,7,7,8,8,10]`，`target = 8` → `[3,4]`；`target = 6` → `[-1,-1]`。

```python
from bisect import bisect_left, bisect_right

def search_range(nums: list[int], target: int) -> list[int]:
    lo = bisect_left(nums, target)          # 第一个 >= target 的位置
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]                     # 越界或该位置不是 target：不存在
    hi = bisect_right(nums, target) - 1     # 第一个 > target 的位置再减 1 = 最后一个 target
    return [lo, hi]
```
