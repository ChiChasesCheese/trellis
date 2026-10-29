---
id: uth-cpp-vector-2-invalidation
node: cpp.vector
type: qa
step: 2
---
## Q
**扩容后旧指针为什么悬空**｜C++ · std::vector

先取 `int* p = &v[0]`，再 `push_back` 或 `reserve`，之后用 `p` 为什么可能崩？

## A
**背景。** 上一张卡说了：扩容会把元素搬进新的一块内存，旧块被释放。可你之前拿到的地址（指针、引用、迭代器）还指着旧块。

**结构。** 迭代器本质上就是指向连续数组的指针。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 192">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扩容前</text>
<rect x="60" y="22" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="76" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="96" y="22" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="112" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="22" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="148" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="168" y="22" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="184" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="10" y="50" width="40" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="30" y="65.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<line x1="30" y1="50" x2="76" y2="46" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="76,46 70.3,49.2 69.8,43.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">push_back 触发扩容后</text>
<rect x="60" y="106" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="76" y="122.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="96" y="106" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="112" y="122.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="106" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="148" y="122.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="168" y="106" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="184" y="122.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="212" y="122" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧块已释放</text>
<rect x="10" y="134" width="40" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="30" y="149.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<line x1="30" y1="134" x2="76" y2="130" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="76,130 70.3,133.2 69.8,127.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="60" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p 悬空</text>
<rect x="60" y="160" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="76" y="176.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="96" y="160" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="112" y="176.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="160" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="148" y="176.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="168" y="160" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="184" y="176.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="204" y="160" width="32" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="220" y="176.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新块</text>
</svg>
```

**细节。**

- 触发扩容：所有迭代器、指针、引用全部失效，因为元素搬进了新块
- 没扩容的 `push_back`：只有 `end()` 失效
- 中间 `insert` / `erase`：该位置及其后面的迭代器失效
- 实测 `reserve(1000)` 之后，`&w[0]` 与原地址不同（libc++）

**为什么。** 连续内存换来 O(1) 随机访问和缓存友好；`std::list` 地址稳定，但每次访问都要跳指针。

**坑。** 遍历时往同一个 vector 里 `push_back` 是未定义行为；删除要用 `it = v.erase(it)`。

**例题：** LC 283 移动零（同类：LC 27 移除元素）

给数组 `nums`，原地把所有 `0` 移到末尾，非零元素保持原来的相对顺序。例：`[0,1,0,3,12]` → `[1,3,12,0,0]`。和 C++ 的 erase-remove 一样：读指针往前走，写指针只在保留元素时前进，不碰扩容。

```python
def move_zeroes(nums: list[int]) -> None:
    write = 0                                  # nums[:write] 是已经排好的非零元素
    for read in range(len(nums)):
        if nums[read] != 0:
            if write != read:                  # write == read 说明前面还没有零，不用动
                nums[write], nums[read] = nums[read], 0
            write += 1
```
