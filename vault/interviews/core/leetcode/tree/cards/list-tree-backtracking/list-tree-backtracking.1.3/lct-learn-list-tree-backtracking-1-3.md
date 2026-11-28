---
id: lct-learn-list-tree-backtracking-1-3
node: list-tree-backtracking.1.3
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 插入节点**｜学习卡

套路是什么？

## A
**一句话。** 插入节点就是找到「前驱」，然后 `new.next = pre.next; pre.next = new`，先接后断；环形有序表的前驱要么夹在 `p.val <= val <= p.next.val` 之间，要么在最大到最小的断点处。

下图：先让新节点指向后继，再让前驱指向新节点。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="40" y="30" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="104" y="30" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="121.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="232" y="30" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="249.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="74" y1="43.0" x2="103" y2="43.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="103.0,43.0 96.7,46.0 96.7,40.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="138" y1="43" x2="231" y2="43" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="231.0,43.0 224.7,46.0 224.7,40.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="168" y="90" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="185.0" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<line x1="202" y1="96" x2="245.0" y2="57" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="245.0,57.0 242.3,63.5 238.3,59.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="335" y="104" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① new.next = pre.next</text>
<line x1="125.0" y1="57" x2="168" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="168.0,96.0 161.3,94.0 165.3,89.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="104" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② pre.next = new</text>
<text x="121.0" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pre</text>
<text x="170" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先接后断：反过来做，5 那一段就丢了</text>
</svg>

```python
def insert(head, val):               # 循环升序链表，head 可为空
    node = ListNode(val)
    if not head:
        node.next = node             # 空表：自己成环
        return node
    p = head
    while True:
        nxt = p.next
        if p.val <= val <= nxt.val:   # 夹在中间
            break
        if p.val > nxt.val and not nxt.val < val < p.val:
            break                    # 断点（最大 → 最小）处插入
        p = nxt
        if p is head:              # 走了一圈：全部相等
            break
    node.next = p.next             # 先接后继
    p.next = node                  # 再接前驱
    return head
```

**要点。**
- 为什么对？：升序环里只有一处「下降」（最大接最小），`val` 要么落在某对相邻值之间，要么比最大还大或比最小还小，此时都插在断点处。
- 普通有序链表怎么改？：用哨兵 `dummy`，走到 `cur.next.val >= val` 或 `cur.next` 为空为止，然后同样先接后断。

**易错点。**
- 全部节点值相等：`[3,3,3]` 插入 `5`，没有断点也没有夹点，必须靠「回到起点」退出，否则死循环。
- 先断后接：`cur.next = node` 写在前面会丢掉原后继。
- 空表忘记自环：`node.next` 必须指向自己，否则不成环。

**对应题目。** LC 708 循环有序列表的插入
