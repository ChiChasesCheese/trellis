---
slug: rotate-list
---
## Q
**LC 61 旋转链表**｜Medium

把链表向右循环移动 `k` 个位置，返回新头。`k` 可达 `2 * 10^9`。

## A
**一句话。** 先求长度 `n` 并成环，`k %= n`，走 `n - k - 1` 步找到新尾，在此断环。

```python
def rotate_right(head, k):
    if not head or not head.next:
        return head
    n, tail = 1, head
    while tail.next:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head                 # 成环
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None             # 断环
    return new_head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉 `k %= n`：`[0,1,2]`、`k = 4` 得 `[1,2,0]`，应为 `[2,0,1]`，且不报错。
- 走 `n - k` 步：停在新头而不是新尾，`[1,2,3,4,5]`、`k = 2` 得 `[5,1,2,3,4]`。

**追问。**
- 向左旋转 `k` 位？：等价于向右旋转 `n - k % n` 位。
- 为什么不能直接用快慢指针找倒数第 `k` 个？：`k` 可能远大于 `n`，必须先数长度取模。

**同模式。** LC 189 轮转数组、LC 19 删除链表的倒数第 N 个结点、LC 876 链表的中间结点
