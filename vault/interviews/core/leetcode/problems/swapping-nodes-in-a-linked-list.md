---
slug: swapping-nodes-in-a-linked-list
---
## Q
**LC 1721 交换链表中的节点**｜Medium

交换链表正数第 `k` 个与倒数第 `k` 个结点的值（从 1 开始计数），返回头结点。

## A
**一句话。** 先走 `k-1` 步得到正数第 `k` 个 `first`；再让 `fast` 从 `first` 出发、`second` 从头出发同步走，`fast` 到尾时 `second` 就是倒数第 `k` 个，交换两者的值。

**图解。** `k = 2`：`fast` 从 `first` 出发与 `second` 同步走，`fast` 到尾时 `second` 停在倒数第 2 个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 126">
<text x="42" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">链表</text>
<rect x="50" y="12" width="40" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="12" width="40" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="130" y="12" width="40" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="170" y="12" width="40" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="210" y="12" width="40" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="110.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">first</text>
<text x="190.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">second</text>
<text x="230.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">fast</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">k = 2：first 是正数第 2 个</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">fast 到尾时 second 是倒数第 2 个，交换 2 和 4</text>
</svg>

```python
def swap_nodes(head, k):
    first = head
    for _ in range(k - 1):
        first = first.next     # 正数第 k 个
    second, fast = head, first
    while fast.next:           # 两者相距 k-1，同步走到尾
        fast = fast.next
        second = second.next
    first.val, second.val = second.val, first.val
    return head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 先走 `k` 步：会得到第 `k+1` 个，正数要走 `k-1` 步。
- 用 `while fast` 作循环条件：`second` 会多走一步，落在倒数第 `k-1` 个。

**追问。**
- 要求交换结点而不是值？：还要记住两个结点的前驱，注意两者相邻或是同一个结点的情况。
- 为什么一遍就够？：`fast` 与 `second` 的距离固定为 `k-1`，`fast` 到尾时 `second` 离尾也是 `k-1`。

**同模式。** LC 19 删除链表的倒数第 N 个结点、LC 61 旋转链表、LC 24 两两交换链表中的节点
