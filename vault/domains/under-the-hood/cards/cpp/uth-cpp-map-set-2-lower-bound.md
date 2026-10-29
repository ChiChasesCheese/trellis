---
id: uth-cpp-map-set-2-lower-bound
node: cpp.map-set
type: qa
step: 2
---
## Q
**std::lower_bound 查 set 为什么慢了一万倍**｜C++ · std::set

对 `std::set` 做二分查找，写 `s.lower_bound(x)` 和 `std::lower_bound(s.begin(), s.end(), x)` 有什么区别？

## A
**背景。** 二分查找靠“一步跳到中间那格”：数组有下标，随时能跳。树没有下标，想到第 k 个元素只能顺着指针一个一个挪。迭代器（iterator）就是指向容器里某个元素的游标，可以往前、往后挪。

**结构。** 成员函数 `s.lower_bound(x)` 沿红黑树从根往下走；全局算法 `std::lower_bound` 只拿到一对迭代器，只会一格一格往后挪，不知道底下是树。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">成员函数 lower_bound:沿树下降</text>
<line x1="159.71" y1="46.1739" x2="120.29" y2="69.8261" stroke="currentColor" stroke-width="1"/>
<line x1="180.29" y1="46.1739" x2="219.71" y2="69.8261" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="102.318" y1="85.2187" x2="87.6822" y2="102.781" stroke="currentColor" stroke-width="1"/>
<line x1="117.682" y1="85.2187" x2="132.318" y2="102.781" stroke="currentColor" stroke-width="1"/>
<line x1="222.318" y1="85.2187" x2="207.682" y2="102.781" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="237.682" y1="85.2187" x2="252.318" y2="102.781" stroke="currentColor" stroke-width="1"/>
<circle cx="170" cy="40" r="12" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="170" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">40</text>
<circle cx="110" cy="76" r="12" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="110" y="80.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<circle cx="230" cy="76" r="12" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="230" y="80.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60</text>
<circle cx="80" cy="112" r="12" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="80" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<circle cx="140" cy="112" r="12" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="140" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<circle cx="200" cy="112" r="12" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="200" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<circle cx="260" cy="112" r="12" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="260" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">70</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">全局 std::lower_bound:迭代器一格一格 ++</text>
<rect x="12" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<line x1="48" y1="178" x2="58" y2="178" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="58,178 52.0,180.7 52.0,175.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="58" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="76" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<line x1="94" y1="178" x2="104" y2="178" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="104,178 98.0,180.7 98.0,175.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="104" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="122" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<line x1="140" y1="178" x2="150" y2="178" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="150,178 144.0,180.7 144.0,175.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="150" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="168" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">40</text>
<line x1="186" y1="178" x2="196" y2="178" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="196,178 190.0,180.7 190.0,175.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="196" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="214" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<line x1="232" y1="178" x2="242" y2="178" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="242,178 236.0,180.7 236.0,175.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="242" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="260" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60</text>
<line x1="278" y1="178" x2="288" y2="178" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="288,178 282.0,180.7 282.0,175.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="288" y="166" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="306" y="182.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">70</text>
<text x="170" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">查 50:树走 3 步,链表要走 5 步</text>
</svg>
```

**细节。**

- 全局版比较次数虽然是 O(log n)，但迭代器要一步一步挪，总共 O(n) 步
- 实测 20 万元素的 `set`，2000 次查询：成员版约 0.2 毫秒，全局版约 1.7 秒

**为什么。** 通用算法只知道迭代器能做什么（前进、后退），不知道容器是树；成员函数才能利用树结构。

**坑。** 对 `set`、`map` 的二分一律用成员函数；只有 `vector` 这类能按下标直接跳的容器才用全局版。

**例题：** LC 34 在排序数组中查找元素的第一个和最后一个位置（同类：LC 35 搜索插入位置）

给一个升序数组和目标值 `target`，返回 `target` 第一次和最后一次出现的下标，不存在返回 `[-1, -1]`，要求 O(log n)。例：`[5,7,7,8,8,10]`、`target = 8` → `[3,4]`。第一个位置就是 `lower_bound`，最后一个位置是 `upper_bound` 前一格。

```python
import bisect

def search_range(nums: list[int], target: int) -> list[int]:
    left = bisect.bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect.bisect_right(nums, target) - 1
    return [left, right]
```
