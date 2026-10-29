---
id: tlc-remove-zero-sum-consecutive-nodes-from-linked-list-2-code
node: a.remove-zero-sum-consecutive-nodes-from-linked-list
type: qa
step: 2
---
## Q
**LC 1171 从链表中删去总和值为零的连续节点**｜写出 Python 实现

单链表头节点 `head`（`1..1000` 个节点，值 `-1000..1000`）。反复删除和为 `0` 的连续节点序列，直到没有，返回新链表的头；结果不唯一，任意合法即可。要求 `O(n)`。

## A
**思路。** 在头部加哨兵 `dummy`（前缀和 `0`）。第一遍沿链表累加前缀和，用字典记录每个前缀和对应的**最后一个**节点。第二遍再累加一次，对每个节点把 `next` 设为「同前缀和的最后节点」的 `next`，跳过中间和为 `0` 的整段。

```python
def remove_zero_sum_sublists(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)                    # 哨兵：整条链表都被删光时也有地方挂
    last: dict[int, ListNode] = {}               # 前缀和 -> 最后一个取到这个前缀和的节点
    s, node = 0, dummy
    while node:                                  # 第一遍：同一前缀和后出现的覆盖先出现的
        s += node.val
        last[s] = node
        node = node.next
    s, node = 0, dummy
    while node:                                  # 第二遍：从 node 直接跳到同前缀和的最后一个节点之后
        s += node.val
        node.next = last[s].next                 # (node, last[s]] 这一段总和为 0，整段删掉
        node = node.next
    return dummy.next
```

**运行。** `[1,2,-3,3,1]` → `[3, 1]`；`[1,2,3,-3,4]` → `[1, 2, 4]`；`[1,2,3,-3,-2]` → `[1]`；`[0]` → `[]`；`[1,-1]` → `[]`；`[5]` → `[5]`。

**复杂度。** 时间 `O(n)`：两遍线性扫描；空间 `O(n)`：字典最多 `n + 1` 项。

**写法要点。** `ListNode(0, head)` 的第二个参数就是 `next`，一步建好哨兵；`last[s] = node` 直接覆盖，后出现的自然留下，不用判断；`while node:` 利用节点的真值（非 `None`）当循环条件；`node.next = last[s].next` 同时覆盖"无需删除"（`last[s]` 就是自己）和"需要删除"两种情况，不用 `if`；字典的值是节点对象，键是整数，`ListNode` 不需要可哈希。
