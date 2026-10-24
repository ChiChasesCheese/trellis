---
id: tlc-merge-k-sorted-lists-5-alt
node: a.merge-k-sorted-lists
type: qa
step: 5
---
## Q
**LC 23 合并 K 个升序链表**｜另一种解法

合并 `k` 条升序链表（总长度 `N <= 10^4`，`k <= 10^4`），除了最小堆，还有什么 `O(N log k)` 的做法？什么时候选它？

## A
**分治（两两合并）。** 把相邻的两条链表合并成一条，一轮后剩 `ceil(k/2)` 条，共 `log k` 轮；每一轮所有节点各被访问一次，`O(N log k)`，额外空间 `O(1)`。

```python
def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    def merge(a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next

    step = 1
    while step < len(lists):            # 每一轮把相邻两条链表合成一条，轮数 log k
        for i in range(0, len(lists) - step, step * 2):
            lists[i] = merge(lists[i], lists[i + step])
        step *= 2
    return lists[0] if lists else None
```

`[[1,4,5],[1,3,4],[2,6]]` → `[1, 1, 2, 3, 4, 4, 5, 6]`，`[]` → `[]`。

**怎么选。**
- 面试默认先讲堆，再补一句分治；分治版复用「合并两个有序链表」，不依赖 `heapq`，空间 `O(1)`。
- 堆版适合输入是流或外部有序文件：只需同时持有 `k` 个队头。
- 分治版会修改传入的 `lists`；不能改输入时先拷贝。
