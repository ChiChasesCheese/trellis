---
id: tlc-tt-reverse-k-group-variants-5-alt
node: p1.tt-reverse-k-group-variants
type: qa
step: 5
---
## Q
**K 个一组翻转链表的变体**｜另一种解法

不先量长度，用 LC 25 经典的「边走边数 `k` 个」写法，怎样支持「不足 `k` 个的尾部也翻转」？「从尾部开始分组」又怎样借助它实现？什么时候选哪种？

## A
**经典写法：每轮先往后数最多 `k` 个。** 数到 `k` 个就翻；不足 `k` 个时由开关决定翻不翻。**从尾分组：整条翻转、从头分组、再整条翻转回来。**

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def reverse_k_group_classic(head: ListNode | None, k: int, reverse_partial: bool = False) -> ListNode | None:
    """边走边数 k 个的经典写法；reverse_partial 控制不足 k 个的尾部翻不翻。"""
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth, count = group_prev, 0
        while count < k and kth.next:                 # 往后数最多 k 个
            kth, count = kth.next, count + 1
        if count == 0 or (count < k and not reverse_partial):
            break
        group_next = kth.next
        first = group_prev.next
        prev, cur = group_next, first                 # prev 先指向下一组：翻完后组尾自动接上
        while cur is not group_next:
            cur.next, prev, cur = prev, cur, cur.next
        group_prev.next = prev                        # prev 现在是组头（原来的 kth）
        group_prev = first                            # 原来的头成了组尾
    return dummy.next


def reverse_k_group_from_tail(head: ListNode | None, k: int, reverse_partial: bool = False) -> ListNode | None:
    """从尾部分组 = 整条链表翻转 -> 从头分组 -> 再整条翻转回来。"""
    return reverse_list(reverse_k_group_classic(reverse_list(head), k, reverse_partial))
```

`[1,2,3,4,5,6,7,8]`、`k = 3`：`reverse_k_group_classic` 得到 `[3,2,1,6,5,4,7,8]`，`reverse_partial=True` 得到 `[3,2,1,6,5,4,8,7]`；`reverse_k_group_from_tail` 得到 `[1,2,5,4,3,8,7,6]`，`reverse_partial=True` 得到 `[2,1,5,4,3,8,7,6]`。时间 `O(n)`（每个节点被数一次、翻一次），空间 `O(1)`。

**怎么选。**
- 只有「从头分组」的变体，或面试官只给了 LC 25 的基础：经典写法最熟悉，不用量长度。
- 要从尾分组：整条翻转三明治最短，但多扫两遍；已经量过长度时，用「先算大小序列」的写法更直接，一遍就够。
- 组的大小不固定（如 `1, 2, 3, ...`）：只有「先算大小序列」的写法能平移过去。
