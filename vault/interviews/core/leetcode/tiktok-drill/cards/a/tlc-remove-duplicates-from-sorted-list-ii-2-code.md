---
id: tlc-remove-duplicates-from-sorted-list-ii-2-code
node: a.remove-duplicates-from-sorted-list-ii
type: qa
step: 2
---
## Q
**LC 82 删除排序链表中的重复元素 II**｜写出 Python 实现

升序单链表 `head`（结点数 `0..300`，值 `-100..100`）。删除所有值出现不止一次的结点（该值的结点全部删除），返回处理后的链表头。要求一遍扫描、`O(1)` 额外空间。

## A
**思路。** 建哑结点接在 `head` 前，`prev` 指向它。`cur` 从头扫：如果 `cur` 和下一个结点值相同，记下这个值，把所有等于它的结点跳过，然后让 `prev.next` 直接指向段后的结点（`prev` 不动）；否则 `cur` 是唯一值，`prev` 和 `cur` 一起前进。最后返回 `dummy.next`。

```python
def delete_duplicates(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)          # 头结点也可能被删，所以需要哑结点
    prev, cur = dummy, head            # prev：最后一个确认保留的结点
    while cur:
        if cur.next and cur.next.val == cur.val:
            dup = cur.val
            while cur and cur.val == dup:   # 整段重复值一个不留
                cur = cur.next
            prev.next = cur            # 接到段后面；prev 不前进，cur 可能又是新一段的开头
        else:
            prev, cur = cur, cur.next  # cur 是唯一值：确认保留
    return dummy.next
```

运行：`head=[1,2,3,3,4,4,5]` → `[1, 2, 5]`，`head=[1,1,1,2,3]` → `[2, 3]`，`head=[]` → `[]`，`head=[1,1]（全是重复）` → `[]`，`head=[1,1,2,2,3]` → `[3]`。

**复杂度。** 时间 `O(n)`：每个结点至多被访问常数次；空间 `O(1)`（只有几个指针，原地修改）。

**写法要点。** `ListNode(0, head)` 直接把哑结点接到 `head` 前；`prev, cur = cur, cur.next` 用元组赋值同时前进两个指针，右侧先整体求值，不会错用旧 `cur`；内层 `while cur and cur.val == dup` 的第一个条件防止走到 `None`；`if cur.next and cur.next.val == cur.val` 利用短路求值，避免对 `None` 取属性。
