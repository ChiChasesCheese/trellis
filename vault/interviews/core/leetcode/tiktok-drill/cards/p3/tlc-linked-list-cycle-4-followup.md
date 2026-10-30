---
id: tlc-linked-list-cycle-4-followup
node: p3.linked-list-cycle
type: qa
step: 4
---
## Q
**LC 141 环形链表**｜追问

面试官接着问：（1）找到环的**入口节点**（LC 142）？（2）求**环的长度**？（3）这个技巧还能用在哪些不是链表的题上？

## A
1. **环的入口**：先用快慢指针找到相遇点。设入环前长度为 `a`，环长为 `L`，相遇时 `slow` 在环内已走 `c` 步。`slow` 共走 `a + c`，`fast` 走了两倍，`2(a + c) = a + c + kL`（`fast` 多绕了 `k` 圈），所以 `a + c = kL`。也就是从相遇点再走 `a` 步，恰好回到入口。做法：一个指针回到 `head`，另一个留在相遇点，两个都每次一步，再相遇的节点就是入口。

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            ptr = head
            while ptr is not slow:      # 两个指针各走一步，在入口相遇
                ptr, slow = ptr.next, slow.next
            return ptr
    return None
```

2. **环长度**：相遇后固定一个指针，让另一个继续走并计数，再次回到该节点的步数就是 `L`。
3. **非链表场景**：只要有「`x → f(x)`」这样的后继函数，就能判圈。快乐数（LC 202）把「各位数字平方和」当作后继，圈里是 `1` 就是快乐数；寻找重复数（LC 287）把数组 `nums[i]` 当作下标指针，重复的数就是环的入口。

**Python 提醒**：元组赋值 `slow, fast = slow.next, fast.next.next` 右边先全部求值，两个新值都基于旧的指针，写法安全。集合版本 `seen: set[ListNode]` 依赖节点的默认身份哈希，别用 `node.val` 当键。
