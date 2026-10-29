---
id: uth-gaps-intervals-1-overlap
node: gaps.intervals
type: qa
step: 1
---
## Q
**两个预订撞没撞，数据库怎么拦**｜PostgreSQL · 17 范围类型

会议室已被订了 14:00 到 15:00，又来一个 14:30 到 15:30 的预订。数据库怎样保证第二条插不进去？

## A
**背景。** 应用里常见的写法：先查有没有重叠，没有再插入。两个请求同时到达时，都查到「没有」，都插入成功，同一间房订了两次。要让数据库自己拦，它得先能把「一段时间」存成一个值，再会判断「重叠」。

**结构。** 范围类型（range type）把一段时间存成一个值，例如 `tsrange`；运算符 `&&` 判断两段是否重叠；排他约束（exclusion constraint）规定：表里任意两行用 `&&` 比较，结果都不能为真。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<rect x="100" y="28" width="70" height="78" stroke="none" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="34" width="140" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="100" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">已订 14:00-15:00</text>
<rect x="100" y="74" width="140" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">新 14:30-15:30</text>
<text x="135" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">重叠 拒绝</text>
<rect x="170" y="114" width="140" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="240" y="131" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">15:00-16:00 可以</text>
<line x1="30" y1="152" x2="310" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="30" y1="148" x2="30" y2="156" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="30" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">14:00</text>
<line x1="170" y1="148" x2="170" y2="156" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="170" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">15:00</text>
<line x1="310" y1="148" x2="310" y2="156" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="310" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">16:00</text>
</svg>
```

```sql
CREATE TABLE reservation (
  during tsrange,
  EXCLUDE USING GIST (during WITH &&)
);
```

**细节。**

- `[14:00, 15:00)` 里方括号含端点、圆括号不含；用构造函数时省略第三个参数，默认就是 `[)`
- 半开区间让「15:00 结束」和「15:00 开始」不重叠，背靠背的预订合法
- 只拦同一间房：`EXCLUDE USING GIST (room WITH =, during WITH &&)`，其中 `=` 要先装 `btree_gist` 扩展

**例题：** LC 252 会议室（同类：LC 253 会议室 II）

给会议时间数组 `intervals`，`intervals[i] = [start, end]`。一个人要参加所有会议，当且仅当任意两个会议不重叠；在 `t` 结束的会议和在 `t` 开始的会议不算重叠。能参加全部返回 `true`。例：`[[0,30],[5,10],[15,20]]` → `false`，`[[7,10],[2,4]]` → `true`。

```python
from itertools import pairwise

def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals)                          # 按开始时间排序，不改入参
    return all(prev[1] <= cur[0] for prev, cur in pairwise(ordered))
```
