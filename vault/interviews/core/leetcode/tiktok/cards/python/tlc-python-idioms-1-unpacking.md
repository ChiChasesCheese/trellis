---
id: tlc-python-idioms-1-unpacking
node: python.idioms
type: qa
step: 1
---
## Q
**Python 工具箱｜解包、交换与链式比较**

交换两个变量、拆出首尾元素、判断 `x` 在区间内，Python 有哪些地道写法？链表反转里一次赋值完成指针翻转，顺序有什么讲究？

## A
```python
a, b = 1, 2
a, b = b, a                          # 交换：右边先整体求值成元组，再依次赋给左边
first, *mid, last = [1, 2, 3, 4, 5]  # 星号收集中间：mid = [2, 3, 4]
x = 5
print(1 < x < 10, 0 <= x < 3)        # True False：链式比较，等价于 1<x and x<10，x 只求值一次
```

- 右边先全部求值，左边**从左到右**依次赋值。这是 `a[i], a[j] = a[j], a[i]` 能直接交换数组元素的原因。
- 链表反转的一次性写法（LC 206）：

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next   # head.next 必须排在 head 之前
    return prev
```

左边顺序是 `head.next` → `prev` → `head`。如果写成 `head, head.next, prev = ...`，`head` 先被改成下一个节点，随后的 `head.next` 改的就是下一个节点，链表断裂。

- 星号解包也能用在调用和拼接上：`f(*args)`、`[*a, *b]`（比 `a + b` 更通用，可混入任意可迭代对象）。
- 适用：LC 206、25、92 链表指针翻转，数组原地交换（LC 75 荷兰国旗、31 下一个排列）。
- **坑**：只想要首尾却没用星号时，长度不符会抛 `ValueError: too many values to unpack`；不关心的位置用 `_` 占位。
