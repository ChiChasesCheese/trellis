---
id: uth-python-dunder-protocols-1-len-slot
node: python.dunder-protocols
type: qa
step: 1
---
## Q
**len(x)、x[i]、for 背后是什么**｜Python · CPython 3.14

自己写的 `MinHeap` 类，为什么加一个 `__len__` 方法，就能用 `len(heap)`，还能写 `while heap:`？

## A
**背景。** `len` 要同时处理列表、字符串、字典，还要处理你自己写的类。常见做法有两种：每个类型自带一个 `.length()` 方法（Java 风格），或者内置函数里把每种类型写死。Python 选了第三条：约定一批固定名字的特殊方法（special method，名字两头各有两个下划线，俗称 dunder），内置函数和运算符一律去调它们。

**结构。** `len(x)` 就是 `type(x).__len__(x)`。只要类里有这个名字的方法，Python 不关心它是什么类型，这叫鸭子类型（duck typing）：走起来像鸭子，就当鸭子。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="8" y="40" width="88" height="32" rx="3"/>
<rect x="244" y="40" width="88" height="32" rx="3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="126" y="40" width="88" height="32" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="96" y1="56" x2="126" y2="56"/>
<line x1="214" y1="56" x2="244" y2="56"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="126.0,56.0 120.0,59.0 120.0,53.0"/>
<polygon points="244.0,56.0 238.0,59.0 238.0,53.0"/>
</g>
<g fill="currentColor">
<text x="52" y="60">len(h)</text>
<text x="170" y="60">type(h)</text>
<text x="288" y="60">__len__(h)</text>
<text x="170" y="120">去 MinHeap 里找 __len__</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="170" y="100">h 就是 MinHeap 的实例</text>
<text x="170" y="25">内置函数只认方法名</text>
</g>
</g>
</svg>
```

| 你写的 | 实际调用 |
|---|---|
| `len(x)` | `__len__` |
| `x[i]` | `__getitem__` |
| `for v in x` | `__iter__` |
| `v in x` | `__contains__` |
| `a + b` | `__add__` |
| `a < b` | `__lt__` |
| `x()` | `__call__` |

**细节。**

- `__len__` 必须返回不小于 0 的整数，否则 `ValueError: __len__() should return >= 0`。
- 没有 `__bool__` 时，`bool(x)` 就看 `__len__` 是不是 0，所以 `while heap:` 在堆空时自动为假。

**为什么。** 内置函数不必认识任何具体类型，新类型只要加上方法就「入伙」。

**例题：** 手写最小堆（TikTok 变体题）

不用 `heapq`，用 Python 列表实现最小堆类 `MinHeap`：`push(x)` 和 `pop()` 是 `O(log n)`，`peek()` 只看最小值，要有 `__len__`，以及线性建堆 `heapify`；堆为空时 `pop` / `peek` 抛 `IndexError`。例：用 `[5, 3, 8, 1, 9, 2]` 建堆后，连续 `pop` 依次得到 `1, 2, 3, 5, 8, 9`。

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
