---
id: tlc-partition-list-4-followup
node: a.partition-list
type: qa
step: 4
---
## Q
**LC 86 分隔链表**｜追问

面试官接着问：（1）改成三路划分：`< x`、`== x`、`> x`？（2）如果是数组而不是链表，原地划分怎么做，稳定吗？（3）能不能不用哑结点？分别怎么改。

## A
1. **三路划分**：再加一条链、一个哑结点，按 `<`、`==`、`>` 分发，最后依次拼接，仍然只遍历一遍。

```python
def partition_three(head: ListNode | None, x: int) -> ListNode | None:
    heads = [ListNode(), ListNode(), ListNode()]       # 小于、等于、大于
    tails = heads[:]
    node = head
    while node:
        i = 0 if node.val < x else 1 if node.val == x else 2
        tails[i].next = node
        tails[i] = node
        node = node.next
    tails[2].next = None
    tails[1].next = heads[2].next
    tails[0].next = heads[1].next
    return heads[0].next
```

2. **数组原地划分**：荷兰国旗（Dutch national flag，LC 75）或快速排序的 partition，`O(n)` 时间 `O(1)` 空间，但**不稳定**；要稳定只能多开 `O(n)` 的数组，这正是链表版本能做到稳定且 `O(1)` 空间的优势。
3. **不用哑结点**：要单独处理「小链还没有头」「大链还没有头」两种情况，每次追加前判空，最后拼接时还要判「小链是否为空」，代码更长更易错；哑结点把这些判断都消掉了。

**Python 提醒**：`heads[:]` 复制的是列表，两个列表里装的是**同一批**节点对象，之后 `tails[i] = node` 只改 `tails`，不影响 `heads`；写成 `tails = heads` 则两者是同一个列表，`tails[i] = node` 会把头也改掉。
