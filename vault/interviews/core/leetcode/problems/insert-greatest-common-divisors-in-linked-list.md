---
slug: insert-greatest-common-divisors-in-linked-list
---
## Q
**LC 2807 在链表中插入最大公约数**｜Medium

在链表每两个相邻结点之间插入一个新结点，值为两者的最大公约数，返回新链表。

## A
**一句话。** 遍历时在 `cur` 与 `cur.next` 之间接入 `gcd` 结点，然后直接跳到原来的下一个结点。

```python
def insert_greatest_common_divisors(head):
    cur = head
    while cur.next:
        nxt = cur.next
        cur.next = ListNode(gcd(cur.val, nxt.val), nxt)
        cur = nxt              # 跳过刚插入的结点
    return head
```

**复杂度。** 时间 `O(n log V)`，空间 `O(1)`（不计新结点）。

**易错点。**
- 插入后 `cur = cur.next`：会走到新结点，下一轮又在新结点后插入，死循环。
- 先改 `cur.next` 再取 `nxt`：原来的下一个结点就丢了。

**追问。**
- `gcd` 怎么算？：辗转相除 `gcd(a, b) = gcd(b, a % b)`，`b = 0` 时为 `a`。
- 递归写法？：先处理 `head.next` 后面的部分，再把 `gcd` 结点接在 `head` 与它之间。

**同模式。** LC 24 两两交换链表中的节点、LC 1669 合并两个链表
