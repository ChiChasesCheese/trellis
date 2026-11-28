---
id: lct-learn-list-tree-backtracking-1-7
node: list-tree-backtracking.1.7
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 双指针**｜学习卡

套路是什么？

## A
**一句话。** 不新建节点：每条结果链留一个哨兵和尾指针，扫一遍把节点挂到对应链尾、最后断尾拼接；两链求相交则各走完自己再走对方，路程拉齐。

下图：每条结果链一个哨兵加一个尾指针；扫完断开大链尾，再把小链尾接到大链头。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="10" y="20" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原链 3 → 1 → 4 → 2，x = 3</text>
<rect x="50" y="36" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="65.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">S</text>
<rect x="100" y="36" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="150" y="36" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="165.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="80" y1="49.0" x2="99" y2="49.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,49.0 92.7,52.0 92.7,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="130" y1="49.0" x2="149" y2="49.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.0,49.0 142.7,52.0 142.7,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="50" y="96" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="65.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">L</text>
<rect x="100" y="96" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="150" y="96" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="165.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<line x1="80" y1="109.0" x2="99" y2="109.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,109.0 92.7,112.0 92.7,106.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="130" y1="109.0" x2="149" y2="109.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.0,109.0 142.7,112.0 142.7,106.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="14" y="54" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">small</text>
<text x="14" y="114" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">large</text>
<text x="165.0" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s（尾）</text>
<text x="165.0" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">l（尾）</text>
<path d="M 180 62 C 210 80, 105 80, 110 96" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="110.0,96.0 105.2,90.9 110.8,89.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="205" y="82" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s.next = large.next</text>
<line x1="180" y1="109" x2="206" y2="109" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="206.0,109.0 199.7,112.0 199.7,106.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="210" y="113" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">None：必须断开</text>
<text x="170" y="154" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扫一遍，每个节点挂到对应链的尾巴上</text>
</svg>

```python
def partition(head, x):              # LC 86
    small = s = ListNode()           # 两个哨兵，s、l 是各自的尾
    large = l = ListNode()
    while head:
        if head.val < x:
            s.next = head            # 挂到小链尾
            s = head
        else:
            l.next = head            # 挂到大链尾
            l = head
        head = head.next
    l.next = None                    # 大链尾可能还连着原节点，必须断开
    s.next = large.next              # 小链接大链
    return small.next
def intersection(a, b):              # LC 160
    p, q = a, b
    while p is not q:
        p = p.next if p else b       # 走完自己，换到对方的头
        q = q.next if q else a
    return p                         # 无交点时同为 None
```

**要点。**
- 为什么对？：每个节点只挂一次，链内顺序就是原顺序，所以稳定；哨兵让「第一个节点」与后面的节点用同一行代码。
- 为什么相交链表会会合？：`p` 走 `a + c + b`，`q` 走 `b + c + a`，同时到交点；无交点时同走 `a + b` 步后一起变 `None`，不会死循环。
- LC 328 怎么改？：不另建哨兵，用头和第二个节点作奇偶两条链的头，循环条件 `even and even.next`，最后 `odd.next = even_head`。

**易错点。**
- LC 86 忘了 `l.next = None`：`[1,4,3,2,5,2]`、`x = 3` 应得 `[1,2,2,4,3,5]`，漏断会成环。
- LC 328 忘了保存 `even_head`：奇数链走完后找不到偶数链的头；`[1,2,3,4,5]` 应得 `[1,3,5,2,4]`。
- LC 160 比较值而不是节点：要用 `is`，值相同的两条独立链不相交。

**对应题目。** LC 328 奇偶链表、LC 86 分隔链表、LC 160 相交链表
