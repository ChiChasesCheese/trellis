---
slug: tt-array-min-heap
---
## Q
**手写最小堆**｜Medium

不用 `heapq`，用列表实现 `MinHeap`：`push`、`pop`（返回并删除最小值）、`peek`、`__len__`，以及 `O(n)` 的 `heapify`；空堆 `pop` / `peek` 抛 `IndexError`。

## A
**一句话。** 完全二叉树按层存进列表，`push` 放末尾后上浮，`pop` 把末尾放到根后下沉到较小的孩子，`heapify` 从最后一个非叶子节点倒着下沉。

```python
class MinHeap:
    # 下标 i：父 (i-1)//2，孩子 2i+1、2i+2
    def __init__(self, items=()):
        self.a = []
        self.heapify(items)

    def __len__(self):
        return len(self.a)

    def peek(self):
        if not self.a:
            raise IndexError("peek from empty heap")
        return self.a[0]

    def push(self, x):
        self.a.append(x)
        self._up(len(self.a) - 1)

    def pop(self):
        if not self.a:
            raise IndexError("pop from empty heap")
        last = self.a.pop()          # 先取走末尾，数组保持连续
        if not self.a:
            return last
        top, self.a[0] = self.a[0], last
        self._down(0)
        return top

    def heapify(self, items):
        self.a = list(items)
        for i in range(len(self.a) // 2 - 1, -1, -1):
            self._down(i)            # 倒着下沉：O(n)

    def _up(self, i):
        a, x = self.a, self.a[i]
        while i > 0:
            p = (i - 1) // 2
            if not x < a[p]:
                break
            a[i] = a[p]              # 父下移，留空位，不做交换
            i = p
        a[i] = x

    def _down(self, i):
        a, n, x = self.a, len(self.a), self.a[i]
        while (c := 2 * i + 1) < n:
            if c + 1 < n and a[c + 1] < a[c]:
                c += 1               # 取较小的孩子
            if not a[c] < x:
                break
            a[i] = a[c]
            i = c
        a[i] = x
```

**复杂度。** `push`、`pop` `O(log n)`，`peek` `O(1)`，`heapify` `O(n)`，空间 `O(n)`。

**易错点。**
- 下沉只和左孩子比：堆 `[1,5,2,6,7,3,4]` 第二次 `pop` 得 `4`，应为 `2`。
- 建堆正着下沉：`[4,3,2,1]` 建出的不是堆，连续 `pop` 得 `[2,1,3,4]`。
- `pop` 先写根再取末尾：只剩一个元素时数组已空，`a[0] = last` 越界。

**追问。**
- 最大堆或带优先级？：存 `(-优先级, 序号, 值)`，序号避免比较不可比的值。
- Top-K？：维护大小为 `k` 的最小堆，`O(n log k)`。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 347 前 K 个高频元素、LC 23 合并 K 个升序链表、LC 295 数据流的中位数
