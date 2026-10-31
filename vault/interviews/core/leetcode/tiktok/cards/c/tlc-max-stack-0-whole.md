---
id: tlc-max-stack-0-whole
node: c.max-stack
type: qa
---
## Q
**LC 716 最大栈**｜Hard · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 7 次 · 最近 2022-08-24（国内 CodeTop）

设计 `MaxStack` 类，既支持栈操作又能查最大元素：`push(x)` 压入；`pop()` 移除并返回栈顶；`top()` 返回栈顶；`peekMax()` 返回栈中最大元素；`popMax()` 移除并返回最大元素，如果有多个最大元素，只移除**最靠近栈顶**的那个。`-10^7 <= x <= 10^7`，所有操作合计最多 `10^4` 次，调用 `pop/top/peekMax/popMax` 时栈非空。进阶：`top` 为 `O(1)`，其余为 `O(log n)`。例：依次 `push(5), push(1), push(5)`，`top()` → `5`，`popMax()` → `5`（移除的是栈顶那个 5，栈变成 `[5, 1]`），`top()` → `1`，`peekMax()` → `5`，`pop()` → `1`，`top()` → `5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 栈里每个元素带唯一编号，另用一个最大堆存 `(值, 编号)`，两边各自惰性删除：被另一边删掉的元素，等它浮到顶部时再丢弃。

**识别。** 「栈顶和全局最大都要快速访问、还要删除中间元素」：一个结构只能高效取一端，所以用两个结构，并解决「同一元素在两边同步删除」的问题，答案是惰性删除（lazy deletion）。

**推导。** 只有 `push/pop/top/peekMax` 时，每个栈元素带一个「截至此处的最大值」就够了（LC 155）；`popMax` 要删栈中间，数组要整体左移或重建。洞察：给元素编号，删除时只把编号记入 `removed`，不立刻从另一个结构里找出来。堆按 `(-值, -编号)` 排序，值相同时编号大的（更靠近栈顶）先出，满足「移除最靠近栈顶的最大值」。每个元素在每个结构里最多被丢弃一次，所以摊还 `O(log n)`。

**简单解法。** 只用一个列表，`peekMax` 与 `popMax` 线性扫描。

```python
class MaxStackSimple:
    def __init__(self) -> None:
        self.stack: list[int] = []

    def push(self, x: int) -> None:
        self.stack.append(x)

    def pop(self) -> int:
        return self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def peekMax(self) -> int:
        return max(self.stack)

    def popMax(self) -> int:
        m = max(self.stack)
        i = len(self.stack) - 1 - self.stack[::-1].index(m)   # 从栈顶往下找第一个最大值
        return self.stack.pop(i)
```

`peekMax` 与 `popMax` 是 `O(n)`；总共 `10^4` 次操作最坏 `10^8` 量级的元素访问，是能过的面试答案。它不满足进阶要求的 `O(log n)`，堆版本才满足。

最优解：

```python
from heapq import heappop, heappush


class MaxStack:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []   # (值, 编号)，栈顶在末尾
        self.heap: list[tuple[int, int]] = []    # (-值, -编号)：值大优先，值相同时编号大（更靠近栈顶）优先
        self.removed: set[int] = set()           # 已被任一边删除的编号
        self.next_id = 0

    def push(self, x: int) -> None:
        self.stack.append((x, self.next_id))
        heappush(self.heap, (-x, -self.next_id))
        self.next_id += 1

    def _trim_stack(self) -> None:               # 栈顶若已被 popMax 删掉，丢弃
        while self.stack[-1][1] in self.removed:
            self.stack.pop()

    def _trim_heap(self) -> None:                # 堆顶若已被 pop 删掉，丢弃
        while -self.heap[0][1] in self.removed:
            heappop(self.heap)

    def pop(self) -> int:
        self._trim_stack()
        x, i = self.stack.pop()
        self.removed.add(i)                      # 堆里那份留给 _trim_heap 清理
        return x

    def top(self) -> int:
        self._trim_stack()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        self._trim_heap()
        return -self.heap[0][0]

    def popMax(self) -> int:
        self._trim_heap()
        neg_x, neg_i = heappop(self.heap)
        self.removed.add(-neg_i)                 # 栈里那份留给 _trim_stack 清理
        return -neg_x
```

运行：示例序列 `push(5), push(1), push(5), top, popMax, top, peekMax, pop, top` 依次输出 `5, 5, 1, 5, 1, 5`；`push(1), push(3), push(2)` 后 `popMax()` → `3`，`top()` → `2`，`pop()` → `2`，`pop()` → `1`。

**复杂度。** `push`、`popMax`、`peekMax` 摊还 `O(log n)`，`pop`、`top` 摊还 `O(1)`（`pop` 的堆侧清理不在这里发生），空间 `O(n)`。

**拓展优化。**
- 最坏情况（非摊还）`O(log n)`：双向链表存栈、平衡树（按值分桶，每桶存节点）存最大值；Python 标准库没有有序容器，面试里讲清楚思路即可，需要时用第三方 `sortedcontainers.SortedDict`。
- 只有 `peekMax` 没有 `popMax` 时退化为 LC 155：每个元素附带「到此为止的最大值」，全部 `O(1)`。

**易错点。**
- 堆只存值不存编号：`popMax` 时无法告诉栈该删哪一个，值相同时更无法区分「最靠近栈顶」的那个。
- 堆键用 `(-值, 编号)` 而不是 `(-值, -编号)`：值相同时编号小（更深）的先出，`push(5), push(1), push(5), popMax` 之后栈会变成 `[1, 5]`，应该是 `[5, 1]`。
- `top` 与 `pop` 忘记先清理栈顶的已删元素：返回已经被 `popMax` 删掉的值。

**追问。**
- 同时要 `popMin / peekMin`：再加一个最小堆，惰性删除共用同一个 `removed`。
- 内存随操作无限增长：`removed` 里的编号一旦在两个结构里都被丢弃就可以移除，需要对每个编号计数。

**同模式。** LC 155 最小栈、LC 895 最大频率栈、LC 146 LRU 缓存、LC 480 滑动窗口中位数（惰性删除）、LC 239 滑动窗口最大值。
