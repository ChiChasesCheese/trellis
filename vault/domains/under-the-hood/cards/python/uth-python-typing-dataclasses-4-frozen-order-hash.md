---
id: uth-python-typing-dataclasses-4-frozen-order-hash
node: python.typing-dataclasses
type: qa
step: 4
---
## Q
**frozen、order 怎样牵出 __hash__**｜Python · CPython 3.14

想把 dataclass 对象放进 `set`、当 `dict` 的键，或者用 `<` 排序，要加哪些选项？

## A
**背景。** 集合和字典靠 `__hash__` 找位置，排序靠 `<`。可变对象的字段一改，哈希值就变，放进集合后就再也找不到它，所以 Python 对「定义了 `__eq__` 又可变」的类，默认不给哈希。

**结构。** 默认的 `@dataclass`（`eq=True`）把 `__hash__` 设成 `None`，对象放不进 `set`。由两个开关决定：

| 选项 | `__hash__` |
|---|---|
| `eq=True`（默认）、`frozen=False`（默认） | `None`，不可哈希 |
| `eq=True`、`frozen=True` | 按字段元组生成 |
| `eq=False` | 沿用父类的（默认按对象身份） |

**细节。**

- `frozen=True` 靠生成的 `__setattr__` / `__delattr__` 抛 `FrozenInstanceError` 来实现。
- `order=True` 生成 `__lt__` 等方法，比较的是字段元组 `(self.a, self.b) < (other.a, other.b)`，所以字段顺序就是排序优先级；两边的类必须相同。

```python
@dataclass(order=True)
class Item:
    val: int
    i: int
# Item(1, 0) < Item(1, 1)：先比 val，再比 i，和元组 (val, i) 一样
```

**坑。** 堆里放 `(val, node)` 元组是同一条比较规则：`val` 相同时会去比 `node`，`node` 不能比大小就抛 `TypeError`，要在中间塞一个唯一编号。

**例题：** LC 23 合并 K 个升序链表

把 `k` 条升序链表合并成一条升序链表。用最小堆装各链表的队头，每次弹出最小的接到结果后面。下面代码里堆元素是 `(值, 链表编号, 结点)`，编号挡在结点前面，值相同时就不会去比较 `ListNode`。

```python
import heapq

class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]  # i 打破 val 相同时的比较
    heapq.heapify(heap)
    dummy = ListNode()
    tail = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```
