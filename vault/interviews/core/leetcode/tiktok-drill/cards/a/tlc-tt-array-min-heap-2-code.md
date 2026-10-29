---
id: tlc-tt-array-min-heap-2-code
node: a.tt-array-min-heap
type: qa
step: 2
---
## Q
**手写最小堆**｜写出 Python 实现

不用 `heapq`，用列表实现 `MinHeap`：`push`、`pop`（返回最小值）、`peek`、`__len__`、线性建堆 `heapify`；`push` / `pop` 为 `O(log n)`，建堆为 `O(n)`；空堆 `pop` / `peek` 抛 `IndexError`；元素个数至多 `10^5`。

## A
**思路。** 列表存完全二叉树，维护“父不大于子”。`push` 追加到末尾后上浮；`pop` 取走末尾元素放到根，再下沉到较小孩子；`heapify` 从最后一个非叶子节点倒着下沉。上浮和下沉都用“空位”写法：先取出要移动的元素 `x`，沿路径把别的元素挪开，最后把 `x` 一次写入，省掉一半赋值。

```python
from collections.abc import Iterable


class MinHeap[T]:
    """数组存完全二叉树：下标 i 的父节点是 (i - 1) // 2，子节点是 2i + 1、2i + 2。元素需支持 <。"""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self.a: list[T] = []
        self.heapify(items)

    def __len__(self) -> int:
        return len(self.a)

    def peek(self) -> T:
        if not self.a:
            raise IndexError("peek from empty heap")
        return self.a[0]

    def push(self, x: T) -> None:
        self.a.append(x)
        self._sift_up(len(self.a) - 1)

    def pop(self) -> T:
        if not self.a:
            raise IndexError("pop from empty heap")
        last = self.a.pop()                  # 先取走最后一个元素，数组保持连续
        if not self.a:
            return last
        top, self.a[0] = self.a[0], last     # 把它放到根，再下沉
        self._sift_down(0)
        return top

    def heapify(self, items: Iterable[T]) -> None:
        self.a = list(items)
        for i in range(len(self.a) // 2 - 1, -1, -1):   # 从最后一个非叶子节点倒着下沉：O(n)
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        a, x = self.a, self.a[i]
        while i > 0:
            parent = (i - 1) // 2
            if not x < a[parent]:            # 只用 <，和 heapq 一致
                break
            a[i] = a[parent]                 # 父节点下移，留一个“空位”，不做交换
            i = parent
        a[i] = x

    def _sift_down(self, i: int) -> None:
        a, n, x = self.a, len(self.a), self.a[i]
        while (child := 2 * i + 1) < n:
            if child + 1 < n and a[child + 1] < a[child]:
                child += 1                   # 取较小的孩子
            if not a[child] < x:
                break
            a[i] = a[child]                  # 较小的孩子上移
            i = child
        a[i] = x
```

运行：`MinHeap([5, 3, 8, 1, 9, 2])` 内部数组 `[1, 3, 2, 5, 9, 8]`，`peek()` → `1`，`len` → `6`，连续 `pop` → `[1, 2, 3, 5, 8, 9]`；元组 `[(2, 'b'), (1, 'z'), (1, 'a')]` 依次弹出 `(1, 'a'), (1, 'z'), (2, 'b')`；空堆 `pop()` → `IndexError`；`10^5` 个随机浮点数逐个 `push` 再全部 `pop`，结果与 `sorted` 一致。

**复杂度。** `push`、`pop` 都是 `O(log n)`：沿一条根到叶的路径走，至多树高 `log n` 步；`peek` 是 `O(1)`；`heapify` 是 `O(n)`；空间 `O(n)`。

**写法要点。** `class MinHeap[T]` 是 3.12 的泛型语法，元素只需支持 `<`；比较只用 `<`，和 `heapq` 的约定一致，自定义对象只要实现 `__lt__`；海象 `(child := 2 * i + 1) < n` 把“算孩子下标”和“判越界”合成一步；`heapify` 里 `list(items)` 复制一份，不改调用者的列表（`heapq.heapify` 是原地改）；私有方法以 `_` 开头，对外只留五个接口。
