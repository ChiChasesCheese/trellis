---
id: lct-learn-data-structures-8-5
node: data-structures.8.5
type: qa
step: 1
---
## Q
**常用数据结构 › 树状数组和线段树 › 动态开点线段树**｜学习卡

套路是什么？

## A
**一句话。** 值域很大（如 `10^9`）建不起完整线段树时，节点用到才创建：只给被操作区间路径上的节点开空间，每次操作 `O(log 值域)`，总空间 `O(操作数 * log 值域)`。

下图：值域 `[0, 10^9)` 的线段树只把被操作区间路径上的节点放进集合，其余节点根本不存在。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<line x1="170" y1="34" x2="95" y2="58" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170" y1="34" x2="245" y2="58" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="95" y1="82" x2="55" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="95" y1="82" x2="135" y2="106" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="55" y1="130" x2="35" y2="154" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="55" y1="130" x2="75" y2="154" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="22" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="95" cy="70" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="245" cy="70" r="13" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="245" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<circle cx="55" cy="118" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="55" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="135" cy="118" r="13" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="135" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<circle cx="35" cy="166" r="13" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="35" y="170" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<circle cx="75" cy="166" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="75" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="195" y="26" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[0, 10⁹)</text>
<text x="180" y="120" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">实线：用到才创建</text>
<text x="180" y="138" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚线：从没碰过，不占空间</text>
<text x="180" y="156" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子编号 2o、2o+1</text>
</svg>

```python
class MyCalendar:                    # 值域 [0, 10^9)
    def __init__(self):
        self.busy = set()            # 动态开点：只记有用的节点
        self.full = set()            # 整段都被占的节点
    def hit(self, o, lo, hi, l, r):  # [l, r) 与已占用相交？
        if r <= lo or hi <= l or o not in self.busy:
            return False
        if o in self.full or (l <= lo and hi <= r):
            return True
        mid = (lo + hi) // 2         # 孩子下标 2o、2o+1
        return (self.hit(2 * o, lo, mid, l, r) or
                self.hit(2 * o + 1, mid, hi, l, r))
    def add(self, o, lo, hi, l, r):
        self.busy.add(o)
        if l <= lo and hi <= r:
            self.full.add(o)
            return
        mid = (lo + hi) // 2
        if l < mid: self.add(2 * o, lo, mid, l, r)
        if mid < r: self.add(2 * o + 1, mid, hi, l, r)
```

**要点。**
- 为什么对？：区间 `[l, r)` 在线段树上拆成 `O(log N)` 个整段节点，路径上的祖先标 `busy`；没出现过的节点不存在，就是「空」，查询遇到就返回不相交。
- LC 729 的更短做法怎么改？：已接受日程互不重叠，用有序的 `starts` 数组，`bisect_left(starts, end)` 找位置，只和前一个日程比结束时间。
- 要支持重叠计数怎么改？：节点存最大重叠数和懒标记（LC 731 / 732），`add` 时区间加一，查询取区间最大值。

**易错点。**
- 区间当闭区间：`[10, 20)` 与 `[20, 30)` 应不冲突，约定半开区间，`r <= lo or hi <= l` 才是不相交。
- 忘了 `full` 的短路：整段已占的节点没有孩子，往下找会误判为空；`hit` 遇到 `full` 必须直接返回 `True`。
- 对 `book` 的失败操作改了树：先 `hit` 再 `add`，失败的预订不能留下痕迹。

**对应题目。** LC 729 我的日程安排表 I
