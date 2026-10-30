---
id: tlc-tt-array-min-heap-0-whole
node: p4.tt-array-min-heap
type: qa
---
## Q
**手写最小堆**｜Medium · 近一年被问：美国 2 次、国内 0 次 · 最近 2026-10-04（面试记录）

不用 `heapq`，用 Python 列表实现最小堆类 `MinHeap`：`push(x)`、`pop()`（返回并删除最小值）、`peek()`（只看最小值）、`__len__`，以及从一个列表线性建堆的 `heapify`。`push` / `pop` 要 `O(log n)`，建堆要 `O(n)`；堆为空时 `pop` / `peek` 抛 `IndexError`。元素个数至多 `10^5`。

例：用 `[5, 3, 8, 1, 9, 2]` 建堆后内部数组是 `[1, 3, 2, 5, 9, 8]`，连续 `pop` 依次得到 `1, 2, 3, 5, 8, 9`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把完全二叉树按层存进列表（下标 `i` 的父节点是 `(i - 1) // 2`，孩子是 `2i + 1`、`2i + 2`），只维护“父不大于子”：`push` 放到末尾后**上浮**，`pop` 把末尾元素放到根后**下沉**到较小的孩子，`heapify` 从最后一个非叶子节点倒着下沉。

**识别。** 「不用 `heapq`」「`push` / `pop` 是 `O(log n)`」就是二叉堆；「线性建堆 `O(n)`」指自底向上的下沉建堆（Floyd 建堆），不是 `n` 次 `push`（那是 `O(n log n)`）。用数组存树是因为完全二叉树没有空洞，下标算术可以代替指针。

**推导。** 暴力：有序数组，`pop` 是 `O(1)` 但 `push` 要插入，`O(n)`；无序数组，`push` 是 `O(1)` 但 `pop` 要找最小值，`O(n)`。浪费：我们只关心最小值，不需要全序。洞察：只保持“父不大于子”这一个局部序，最小值自然在根；完全二叉树高度是 `log n`，一次修复只沿一条根到叶的路径走，所以是 `O(log n)`。建堆为什么是 `O(n)`：叶子（约一半的节点）本来就是堆，只有非叶子要下沉，下沉代价等于它到叶子的高度，高度为 `h` 的节点约 `n / 2^(h+1)` 个，总和 `Σ h · n / 2^(h+1)` 是 `O(n)`。

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

运行：`MinHeap([5, 3, 8, 1, 9, 2])` 内部数组 `[1, 3, 2, 5, 9, 8]`，`peek()` → `1`，`len` → `6`，连续 `pop` → `[1, 2, 3, 5, 8, 9]`；元组 `[(2, 'b'), (1, 'z'), (1, 'a')]` 依次弹出 `(1, 'a'), (1, 'z'), (2, 'b')`；空堆 `pop()` → `IndexError`。

**复杂度。** `push`、`pop` 都是 `O(log n)`（沿一条路径走，至多树高 `log n` 步），`peek` 是 `O(1)`，`heapify` 是 `O(n)`，空间 `O(n)`。

**易错点。**
- 下沉必须和**较小**的孩子比较。只和左孩子比：对堆 `[1, 5, 2, 6, 7, 3, 4]`，第一次 `pop` 返回 `1`，末尾的 `4` 放到根后因为左孩子 `5` 不比它小就停了；第二次 `pop` 返回 `4`，正确是 `2`。
- 建堆必须倒着下沉：正着从下标 `0` 往后下沉，`[4, 3, 2, 1]` 建出的数组不是堆，连续 `pop` 得到 `[2, 1, 3, 4]`，正确是 `[1, 2, 3, 4]`。
- `pop` 里先取走末尾元素再写根：只剩一个元素时数组已空，不先返回会在 `self.a[0] = last` 上越界。

**追问。**
- 用它排课：Kahn 拓扑排序里把“入度为 0 的队列”换成最小堆，每次先上编号最小的课，得到字典序最小的上课顺序，有环时输出不足 `n` 门就返回空列表，`O((n + m) log n)`。
- 最大堆或带优先级的元素：存 `(-优先级, 序号, 值)` 元组，序号用来避免比较不可比较的值。
- Top-K：维护大小为 `k` 的最小堆，`O(n log k)`。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 347 前 K 个高频元素、LC 23 合并 K 个升序链表、LC 295 数据流的中位数、LC 207 / 210 课程表、LC 253 会议室 II。
