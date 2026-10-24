---
id: tlc-sort-list-2-code
node: a.sort-list
type: qa
step: 2
---
## Q
**LC 148 排序链表**｜写出 Python 实现

链表头结点 `head`（节点数 `[0, 5 * 10^4]`，值在 `[-10^5, 10^5]`），按升序排好并返回新的头结点，要求真正重排节点，时间 `O(n log n)`。

## A
**思路。** 链表长度小于 2 时已经有序，直接返回。否则用快慢指针找到前半段的末尾，在那里断开，得到两条链表。递归排序两条链表，再用合并两个有序链表的函数合并。

```python
def sort_list(head: ListNode | None) -> ListNode | None:
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

    if not head or not head.next:
        return head
    slow, fast = head, head.next        # fast 先走一步：偶数长度时 slow 停在前半段末尾
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None    # 断开成两半
    return merge(sort_list(head), sort_list(mid))
```

运行：`[4,2,1,3]` → `[1, 2, 3, 4]`，`[-1,5,3,4,0]` → `[-1, 0, 3, 4, 5]`，`[]` → `[]`，`[1]` → `[1]`，`5 * 10^4` 个随机数、逆序数、全相同的数都能正确排序；值相同的节点保持原来的先后顺序（稳定）。

**复杂度。** 时间 `O(n log n)`：递归深度 `log n`，每层的断开和合并共 `O(n)`；空间 `O(log n)`：递归栈。

**写法要点。** `merge` 定义成内层函数，只在这里用，名字不污染外面；`slow, fast = head, head.next` 的起点让偶数长度的链表平分，奇数长度时前半段多一个，保证两半都比原链表短，递归一定终止；`mid, slow.next = slow.next, None` 一条元组赋值同时取出后半段的头并断开，右边先求值，所以 `mid` 拿到的是断开之前的 `slow.next`；`tail.next = a or b` 一次挂上剩余的整段。
