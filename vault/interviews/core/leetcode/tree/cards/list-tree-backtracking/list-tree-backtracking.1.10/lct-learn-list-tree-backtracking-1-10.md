---
id: lct-learn-list-tree-backtracking-1-10
node: list-tree-backtracking.1.10
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 综合应用**｜学习卡

套路是什么？

## A
**一句话。** 哈希表负责 `O(1)` 定位，双向链表（带哨兵）负责 `O(1)` 摘下和插入：表存「键 → 节点」，链表按「最近使用」或「计数」排序，每个操作都是定位、摘下、放到新位置。

下图：哈希表 `O(1)` 定位节点，双向链表 `O(1)` 摘下和插入；头旧尾新。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<text x="10" y="22" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希表</text>
<rect x="92" y="10" width="36" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="25" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">k1</text>
<line x1="110" y1="32" x2="110" y2="76" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="110.0,76.0 107.0,69.7 113.0,69.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="152" y="10" width="36" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="25" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">k2</text>
<line x1="170" y1="32" x2="170" y2="76" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="170.0,76.0 167.0,69.7 173.0,69.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="212" y="10" width="36" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="230" y="25" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">k3</text>
<line x1="230" y1="32" x2="230" y2="76" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="230.0,76.0 227.0,69.7 233.0,69.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="20" y="78" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="45" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">头</text>
<rect x="270" y="78" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="295" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">尾</text>
<rect x="90" y="78" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k1</text>
<rect x="150" y="78" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">k2</text>
<rect x="210" y="78" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">k3</text>
<line x1="70" y1="91" x2="90" y2="91" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,91.0 83.7,94.0 83.7,88.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="70.0,91.0 76.3,88.0 76.3,94.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="130" y1="91" x2="150" y2="91" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,91.0 143.7,94.0 143.7,88.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="130.0,91.0 136.3,88.0 136.3,94.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="190" y1="91" x2="210" y2="91" stroke-width="1.2" stroke="currentColor"/>
<polygon points="210.0,91.0 203.7,94.0 203.7,88.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="190.0,91.0 196.3,88.0 196.3,94.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="250" y1="91" x2="270" y2="91" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,91.0 263.7,94.0 263.7,88.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="250.0,91.0 256.3,88.0 256.3,94.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="45" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最旧</text>
<text x="295" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最新</text>
<path d="M 110 104 C 120 150, 260 150, 268 108" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="268.0,108.0 269.4,114.9 263.6,113.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="190" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">get(k1)：摘下，挪到尾部</text>
<text x="170" y="170" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超容量：逐出头哨兵后面那个</text>
</svg>

```python
class LRUCache:                      # LC 146，OrderedDict 版
    def __init__(self, cap):
        self.cap = cap
        self.d = OrderedDict()       # 链表在这里：头旧尾新

    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)      # 访问 = 挪到最新
        return self.d[key]

    def put(self, key, value):
        self.d[key] = value
        self.d.move_to_end(key)      # 新键或旧键都放到最新
        if len(self.d) > self.cap:
            self.d.popitem(last=False)   # 逐出最旧
```

**要点。**
- 手写双向链表怎么做？：节点存 `key, val, prev, next`，哨兵环 `root.next` 最新、`root.prev` 最旧；`remove(x)` 与 `push_front(x)` 各改四个指针，逐出末尾时靠节点里的 `key` 反查并删表。
- 为什么必须双向？：摘下中间节点要把前驱接到后继，单向链表得遍历才找到前驱；堆做不到 `O(1)` 摘走任意元素。
- LC 460、LC 432 怎么改？：元素从「键」变成「桶」：460 是 `freq → 有序字典` 加 `min_freq`（新键置 `1`，仅当旧桶变空且等于 `min_freq` 才加一）；432 是按计数升序串起的桶链表，`inc/dec` 只在相邻桶间搬，最大最小在两端。
- LC 1171 怎么做？：不是设计题，前缀和加哈希：第一遍记每个前缀和**最后一次**出现的节点，第二遍让 `node.next = last[s].next`，哨兵兜住头被删。

**易错点。**
- 手写节点不存 `key`：容量 `1`、`put(1,1)`、`put(2,2)` 逐出节点 `1` 时没法从表里删，之后 `get(1)` 应得 `-1`。
- `put` 命中旧键没挪到最新：容量 `2`、`put(1,1)`、`put(2,2)`、`put(1,10)`、`put(3,3)` 应逐出键 `2`，`get(1)` 得 `10`。
- LC 1171 第一遍只记第一次出现：`[1,2,-3,3,1]` 应得 `[3,1]`，只记第一次会让指针回跳成环。

**对应题目。** LC 146 LRU 缓存、LC 432 全 O(1) 的数据结构、LC 1171 从链表中删去总和值为零的连续节点、LC 460 LFU 缓存
