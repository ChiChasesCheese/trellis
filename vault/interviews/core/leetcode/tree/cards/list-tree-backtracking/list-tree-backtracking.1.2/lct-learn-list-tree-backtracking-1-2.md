---
id: lct-learn-list-tree-backtracking-1-2
node: list-tree-backtracking.1.2
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 删除节点**｜学习卡

套路是什么？

## A
**一句话。** 删除节点要改的是「前一个节点的 `next`」，所以加一个哨兵头 `dummy`，让头节点也有前驱，循环里看 `cur.next` 决定删不删。

下图：删除改的是前驱的 `next`；哨兵 `dummy` 让头节点也有前驱。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="10" y="50" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="27.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dm</text>
<rect x="64" y="50" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="118" y="50" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="135.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="172" y="50" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="189.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="226" y="50" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="243.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="280" y="50" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="44" y1="63.0" x2="63" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="63.0,63.0 56.7,66.0 56.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="98" y1="63.0" x2="117" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="117.0,63.0 110.7,66.0 110.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="152" y1="63.0" x2="171" y2="63.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="171.0,63.0 164.7,66.0 164.7,60.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<line x1="206" y1="63.0" x2="225" y2="63.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="225.0,63.0 218.7,66.0 218.7,60.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<line x1="260" y1="63.0" x2="279" y2="63.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="279.0,63.0 272.7,66.0 272.7,60.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="27.0" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dummy</text>
<text x="135.0" y="92" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">prev</text>
<path d="M 135 50 C 165 10, 267 10, 297 50" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="297.0,50.0 292.0,45.1 297.6,43.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216.0" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">prev.next = prev.next.next</text>
<text x="170" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">看 prev.next 决定删不删；删完 prev 不动，继续看新的 next</text>
</svg>

```python
def delete_duplicates(head):         # 以删光所有重复值为例（LC 82）
    dummy = ListNode(0, head)        # 头也可能被删，需要哨兵
    prev = dummy                     # prev 是最后一个确定保留的节点
    while prev.next and prev.next.next:
        x = prev.next.val
        if prev.next.next.val == x:  # 有重复，整段值为 x 的都删
            while prev.next and prev.next.val == x:
                prev.next = prev.next.next
        else:
            prev = prev.next
    return dummy.next
```

**要点。**
- 为什么对？：`prev` 之后的第一个节点是否保留，取决于它和后继是否同值；整段删掉后 `prev` 不动，因为新的 `prev.next` 还没检查过。
- LC 83 怎么改？：保留一个，不需要哨兵：`cur.next.val == cur.val` 就 `cur.next = cur.next.next`，否则 `cur = cur.next`。
- LC 237 怎么改？：拿不到前驱，只能把后继的值复制到自己身上，再 `node.next = node.next.next`。
- LC 1669 怎么改？：走到下标 `a - 1` 记为 `before`，走到 `b + 1` 记为 `after`，`before.next` 接 `list2` 头，`list2` 尾接 `after`。

**易错点。**
- 循环条件写 `while cur`：要操作 `cur.next`，条件必须保证 `cur.next` 存在，否则空指针。
- 删完一段还让 `prev` 前进：`[1,2,2,3]` 删掉 `2` 后 `prev` 仍应是 `1`，新的 `prev.next`（`3`）还没检查，前进会跳过它。
- 1669 找尾节点：`list2` 的尾要从头走到 `next` 为空，别忘了。

**对应题目。** LC 237 删除链表中的节点、LC 1669 合并两个链表、LC 82 删除排序链表中的重复元素 II、LC 83 删除排序链表中的重复元素
