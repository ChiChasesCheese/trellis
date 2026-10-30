---
id: tlc-reverse-nodes-in-even-length-groups-2-code
node: b.reverse-nodes-in-even-length-groups
type: qa
step: 2
---
## Q
**LC 2074 反转偶数长度组的节点**｜写出 Python 实现

链表（节点数 `[1, 10^5]`）按 `1, 2, 3, ...` 的长度依次分组，最后一组可能不足预期长度；反转每个**实际长度为偶数**的组，返回头节点，额外空间 `O(1)`。

## A
**思路。** `prev` 是上一组的尾，`size` 是预期长度。每轮先数出本组实际节点数 `count`：偶数就原地反转（累积指针初值取下一组的头），奇数就让 `prev` 前进 `count` 步；然后 `size += 1`。

```python
def reverse_even_length_groups(head: ListNode | None) -> ListNode | None:
    prev = head                                  # 第 1 组只有 1 个节点，奇数，不翻；prev 是上一组的尾
    size = 2
    while prev.next:
        node, count = prev.next, 0
        while node and count < size:             # 数出本组实际有多少节点（最后一组可能不足 size）
            node, count = node.next, count + 1
        if count % 2 == 0:
            first = prev.next
            tail, cur = node, first              # tail 初值取下一组的头：翻完后本组尾自动接上
            for _ in range(count):
                cur.next, tail, cur = tail, cur, cur.next
            prev.next = tail                     # tail 现在是本组的新头
            prev = first                         # 原来的头变成本组的尾
        else:
            for _ in range(count):
                prev = prev.next
        size += 1
    return head
```

运行：`[5,2,6,3,9,1,7,3,8,4]` → `[5, 6, 2, 3, 9, 1, 4, 8, 3, 7]`，`[1,1,0,6]` → `[1, 0, 1, 6]`，`[2,1]` → `[2, 1]`，`[1]` → `[1]`，`[1,...,9]` → `[1, 3, 2, 4, 5, 6, 7, 8, 9]`，`[1,...,10]` → `[1, 3, 2, 4, 5, 6, 10, 9, 8, 7]`，`10^5` 个节点正常返回。

**复杂度。** 时间 `O(n)`：每个节点被数一次、至多被翻一次；空间 `O(1)`。

**写法要点。**
- `cur.next, tail, cur = tail, cur, cur.next`：元组赋值先算好右边三项再从左到右赋值，一行完成「反接并前移」；`cur.next` 必须写在最前，因为它依赖旧的 `cur`。
- 先数后翻：`count` 同时给出奇偶判断和翻转次数，实际长度的问题只在一处解决。
- `node, count = node.next, count + 1` 同时推进两个变量，循环条件 `node and count < size` 同时处理链表结束和组满两种停止。
- `prev = head` 起步，跳过必然为奇数的第一组，不需要哑节点：头节点永远不会被反转。
