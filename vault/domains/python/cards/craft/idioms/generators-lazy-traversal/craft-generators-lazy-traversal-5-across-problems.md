---
id: craft-generators-lazy-traversal-5-across-problems
node: craft.idioms.generators-lazy-traversal
type: qa
step: 5
---
## Q
**生成器与惰性遍历 · 文件搜索、表格、最近门店、外卖里生成器的几种用法**｜写法

文件搜索的前序遍历、表格引擎的区间、最近门店的两侧扩展、外卖的相邻切点，都用了生成器或 `itertools`。它们产出的是什么，惰性换来了什么？

## A
**要点。** 同一个想法：**不预先生成全部，只在被问到时算下一个**。区别在于每个生成器背后的状态：显式栈、一个下标、一个“当前值”的游标。

```python
# amz-linux-find：显式栈，逐个 yield；惰性、不受递归深度限制
while stack:
    entry, ancestors = stack.pop()
    if entry.depth > 0 and flt.matches(entry):
        yield entry
    ...
    for name in sorted(node.children, reverse=True):     # 逆序压栈，弹出时升序
        stack.append(...)

# amz-closest-store：每侧一个生成器，状态是「当前值」，调用方按需推进
def _runs_down(self, start):
    value = self._index.floor(start)
    while value is not None:
        yield value, self._index.count(value)
        value = self._index.floor(value - 1)

# dasher-payout：pairwise 遍历相邻切点
for a, b in pairwise(points):
    mid = a + (b - a) / 2
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

表格引擎的区间也是按需产出格子名，求值和找依赖共用同一个生成器。最近门店里手写的双指针归并，本可以用 `heapq.merge`（见上一张卡）。

**见于。** amz-linux-find、spreadsheet-engine、amz-closest-store、dasher-payout、pub-sub。

**信号。** 一个函数先构造了一个很大的列表，然后调用方只用了开头几项；或者遍历一个递归结构，担心递归深度；或者需要在中途停下来。
