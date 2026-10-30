---
id: tlc-odd-even-linked-list-4-followup
node: p4.odd-even-linked-list
type: qa
step: 4
---
## Q
**LC 328 奇偶链表**｜追问

面试官接着问：（1）按**节点值**的奇偶而不是下标分组？（2）推广到按下标模 `k` 分成 `k` 组？（3）如果输入是「奇数位升序、偶数位降序」的链表，要求整体排成升序？

## A
1. **按值分组**：不能再靠跳指针，改用两个哑头节点（dummy）+ 尾插：遍历每个节点，`node.val % 2` 决定接到哪条链的尾，最后偶链尾置空、奇链尾接偶链头。保序，`O(n)` 时间、`O(1)` 空间。
2. **模 `k` 分组**：`k` 个哑头，下标 `i` 的节点接到第 `i % k` 条链的尾；最后每条尾的 `next` 置空，否则会残留旧指针成环。

```python
def split_mod_k(head: ListNode | None, k: int) -> list[ListNode | None]:
    dummies = [ListNode() for _ in range(k)]
    tails = dummies[:]                 # 每组当前的尾节点
    i = 0
    while head:
        tails[i % k].next = head
        tails[i % k] = head
        head = head.next
        i += 1
    for tail in tails:
        tail.next = None
    return [d.next for d in dummies]
```

3. **奇升偶降排序**：按奇偶下标拆成奇链、偶链；偶链是降序，反转成升序；再用合并两个有序链表（LC 21）。三步都是 `O(n)` 时间、`O(1)` 空间。

**Python 提醒**：`v[0::2]` 这类切片会复制出新列表，只适合做对照，不满足 `O(1)` 空间；`[ListNode()] * k` 会得到 `k` 个同一对象，必须用推导式创建哑头。
