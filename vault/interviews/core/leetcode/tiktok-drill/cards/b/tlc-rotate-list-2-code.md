---
id: tlc-rotate-list-2-code
node: b.rotate-list
type: qa
step: 2
---
## Q
**LC 61 旋转链表**｜写出 Python 实现

把链表（结点数 `0` 到 `500`）循环右移 `k` 位（`0 <= k <= 2 * 10^9`），返回新的头结点。要求 `O(n)` 时间、`O(1)` 额外空间。

## A
**思路。** 第一遍数出长度 `n` 并停在尾结点，`k %= n`。尾接头成环，从头走 `n - k - 1` 步到新尾，新头是它的下一个，把新尾的 `next` 置空断环。

```python
def rotate_right(head: ListNode | None, k: int) -> ListNode | None:
    if head is None or head.next is None or k == 0:
        return head
    # 第一遍：数长度，同时找到尾结点
    n, tail = 1, head
    while tail.next:
        tail = tail.next
        n += 1
    k %= n                                    # k 最大 2*10^9，转一整圈等于没转
    if k == 0:
        return head
    tail.next = head                          # 首尾相连成环
    new_tail = head
    for _ in range(n - k - 1):                # 新尾是原来的第 n-k 个结点
        new_tail = new_tail.next
    new_head = new_tail.next                  # 新头是它的下一个
    new_tail.next = None                      # 在这里断环
    return new_head
```

运行：`[1,2,3,4,5], 2` → `[4,5,1,2,3]`，`[0,1,2], 4` → `[2,0,1]`，`[], 3` → `[]`，`[7], 10^9` → `[7]`，`[1,2], 2 * 10^9` → `[1,2]`。

**复杂度。** 时间 `O(n)`：数长度一遍，找新尾不到一遍；空间 `O(1)`：只改指针，不建新结点。

**写法要点。** `n, tail = 1, head` 用元组赋值同时初始化计数和指针；`for _ in range(...)` 表示只关心步数；`ListNode | None` 是 3.10+ 的联合类型写法，空链表的返回值类型一目了然；`k % n == 0` 时提前返回，不必成环再断开。
