---
id: tlc-python-classes-design-7-typing
node: python.classes-design
type: qa
step: 7
---
## Q
**Python 设计题｜类型注解与设计题的开场套路**

链表 / 树节点类里自引用的类型注解怎么写？设计题动手之前应该先和面试官确认什么？

## A
```python
# 文件第一行写 from __future__ import annotations：注解不立即求值，类内可以直接引用自己
class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next
class Cache:
    def __init__(self, capacity: int) -> None:
        self.index: dict[int, ListNode] = {}     # 内置泛型，3.9+
        self.cap = capacity
```

- Python 3.10+ 用 `X | None` 代替 `Optional[X]`；3.9+ 的 `list[int]`、`dict[str, int]` 代替 `typing.List`。
- 类内部引用自己，加 `from __future__ import annotations`，或写成字符串 `"ListNode"`；没有它，`next: ListNode | None` 在类定义时会报 `NameError`。
- 注解不影响运行，但写清楚能让面试官一眼看到数据结构的形状（`dict[int, ListNode]`），也方便自己发现空值漏判。

设计题的开场四件事（动手写代码之前）：
1. **接口**：有哪些方法、参数与返回值（是否允许重复键、返回 `-1` 还是抛异常）。
2. **复杂度目标**：每个操作要 `O(1)` 还是 `O(log n)`；这决定了数据结构（哈希 + 链表、堆、有序结构）。
3. **约束**：容量、并发（要不要线程安全）、数据规模。
4. **不变量**：写下「哈希表里的键恰好是链表里的节点」这类每次操作后都成立的条件，并在每个方法结束处核对。

适用：LC 146、460、380、432、706、1146 等设计题。
