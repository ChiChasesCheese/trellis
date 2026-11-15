---
slug: delete-n-nodes-after-m-nodes-of-a-linked-list
---
## Q
**LC 1474 删除链表 M 个节点之后的 N 个节点**｜Easy

从头开始，保留 `m` 个结点、删掉接下来的 `n` 个，如此重复直到链表结束，返回头结点。

## A
**一句话。** `cur` 走到要保留的第 `m` 个结点，`nxt` 从它后面再跳过 `n` 个，把 `cur.next` 接到 `nxt`，从 `nxt` 开始下一轮。

```python
def delete_nodes(head, m, n):
    cur = head
    while cur:
        for _ in range(m - 1):     # 走到要保留的第 m 个
            if cur.next is None:
                return head
            cur = cur.next
        nxt = cur.next
        for _ in range(n):         # 跳过后面 n 个
            if nxt is None:
                break
            nxt = nxt.next
        cur.next = nxt             # 删掉中间这段
        cur = nxt
    return head
```

**复杂度。** 时间 `O(L)`，空间 `O(1)`。

**易错点。**
- 保留段走 `m` 步：`cur` 本身就是第 1 个，只需再走 `m-1` 步。
- 跳过时不判空：剩余结点不足 `n` 个时 `nxt.next` 会报错。

**追问。**
- 需要释放被删结点（C/C++）？：跳过时逐个 `delete`，先保存下一个指针再释放。
- 换成「每隔 k 个删一个」？：同样的两段式，`n = 1`。

**同模式。** LC 82 删除排序链表中的重复元素 II、LC 203 移除链表元素、LC 1721 交换链表中的节点
