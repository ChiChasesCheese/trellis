---
id: uth-kafka-log-index-2-warm-section
node: kafka.log-index
type: qa
step: 2
---
## Q
**索引里的“暖区”二分**｜Kafka · 4.0

Kafka 在映射进内存（mmap）的 `.index` 里查找时，为什么不直接做标准二分，而要先看文件末尾的一小段？

## A
**背景。** 操作系统只把最近用过的页留在内存里，没用过的页要从磁盘读（缺页）。标准二分从正中间开始跳，碰到的那几页，会随索引追加出新页而整批更换。换页后的第一次查找要缺页读盘，源码注释记录：生产延迟从几毫秒跳到约 1 秒。

**结构。** `AbstractIndex` 把索引最后 8192 字节划为暖区（warm section，偏移量索引即 1024 项）：目标落在暖区，就只在暖区里二分；否则才去前面二分。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 116">
<text x="332" y="14" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">追上进度的读者几乎只查这里</text>
<line x1="290" y1="20" x2="290" y2="36" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="290,42 287.0,36.0 293.0,36.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="8" y="44" width="240" height="24" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="128" y="60.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前面的历史项</text>
<rect x="248" y="44" width="84" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="290" y="60.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">暖区</text>
<text x="290" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">页常驻缓存</text>
<line x1="100" y1="104" x2="100" y2="76" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polygon points="100,70 103.0,76.0 97.0,76.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="112" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">目标不在暖区才来这里二分</text>
</svg>
```

**细节。** 追上进度的消费者和 follower（备份副本）几乎只查最新位置，所以暖区那几页一直留在页缓存（操作系统缓存磁盘内容的内存）里。

**为什么。** 二分的次数几乎不变，最热的访问却只碰固定的少数几页。

**例题：** LC 704 二分查找

给升序整型数组 `nums`（元素互不相同）和目标值 `target`，存在则返回下标，否则返回 `-1`，要求 O(log n)。例：`nums = [-1,0,3,5,9,12]`，`target = 9` → `4`；`target = 2` → `-1`。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)                  # 搜索区间 [lo, hi)，左闭右开
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1                   # mid 太小，排除 [lo, mid]
        else:
            hi = mid                       # mid 可能就是答案，保留 [lo, mid)
    return lo if lo < len(nums) and nums[lo] == target else -1
```
