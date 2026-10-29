---
id: tlc-partition-list-2-code
node: b.partition-list
type: qa
step: 2
---
## Q
**LC 86 分隔链表**｜写出 Python 实现

单链表 `head`（节点数 `0 ~ 200`，值 `-100 ~ 100`）和整数 `x`：把值 `< x` 的节点全部排到值 `>= x` 的节点前面，两部分内部各自保持原顺序。要求一次遍历，`O(1)` 额外空间。

## A
**思路。** 准备两个哑结点，分别作为「小于 `x`」和「大于等于 `x`」两条链的头，各配一个尾指针。遍历原链，节点按值追加到对应链的尾部；遍历完把大链的尾 `next` 置空，再让小链的尾指向大链的第一个真实节点，返回小链哑结点的 `next`。

```python
def partition(head: ListNode | None, x: int) -> ListNode | None:
    small_dummy, big_dummy = ListNode(), ListNode()    # 两条链各一个哑结点
    small, big = small_dummy, big_dummy                # 各自的尾指针
    node = head
    while node:
        if node.val < x:
            small.next = node
            small = node
        else:
            big.next = node
            big = node
        node = node.next
    big.next = None                                    # 必须断开：大链尾巴原来可能还连着小结点
    small.next = big_dummy.next                        # 小链接上大链
    return small_dummy.next
```

运行：`[1,4,3,2,5,2], x=3` → `[1, 2, 2, 4, 3, 5]`，`[2,1], x=2` → `[1, 2]`，`[], x=0` → `[]`，`[3,1], x=3` → `[1, 3]`，`[1,2,3], x=10（全小于）` → `[1, 2, 3]`。

**复杂度。** 时间 `O(n)`：每个节点只访问一次；空间 `O(1)`：只用两个哑结点和几个指针，节点是原地重新挂接的。

**写法要点。** `ListNode()` 用默认参数建哑结点，`small_dummy.next` 永远是小链真实头，免去「链还是空的」的特判。元组式同时初始化：`small_dummy, big_dummy = ListNode(), ListNode()`；`small, big = small_dummy, big_dummy` 把「头」与「尾指针」分开命名。`while node:` 直接用结点的真值判断结束。循环里 `small.next = node` 之后 `node` 的 `next` 暂时没动，所以最后统一 `node = node.next` 是安全的。
