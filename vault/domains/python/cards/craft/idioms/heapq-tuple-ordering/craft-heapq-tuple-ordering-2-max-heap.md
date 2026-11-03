---
id: craft-heapq-tuple-ordering-2-max-heap
node: craft.idioms.heapq-tuple-ordering
type: qa
step: 2
---
## Q
**heapq 的元组序 · 没有大顶堆时怎么让「大的先出」**｜写法

分账要每次取出欠款最多的人和被欠最多的人，紧急邮件要严重度高的先投递，同级先到先出。`heapq` 只有小顶堆，该怎么做？如果排序键是字符串，没法取相反数怎么办？

## A
**要点。** 数值键存**相反数**：`-severity` 最小的就是 severity 最大的，弹出时再取反。完整元素是 `(-key, 序号, 载荷)`：相反数决定主序，序号保证同级先进先出，载荷永不参与比较。非数值键没法取负，就用一个反转 `__lt__` 的小包装类；只要前 k 个时，`heapq.nlargest(k, items, key=...)` 更省事。

```python
tie = count()

# heapq 只有小顶堆。要「最大的先出」：存相反数，弹出时再取反
creditors: list[tuple[int, int, str]] = []
for name, credit in [("ann", 30), ("bob", 70), ("cy", 70)]:
    heapq.heappush(creditors, (-credit, next(tie), name))   # 相反数 + 序号 + 载荷

# 严重度大的先出，同级先到先出
mail: list[tuple[int, int, str]] = []
for sev, msg in [(1, "low"), (3, "fire"), (3, "flood"), (2, "wind")]:
    heapq.heappush(mail, (-sev, next(tie), msg))

print("债权人(金额大的先):", [(-c, n) for c, _, n in sorted(creditors)])
print("紧急邮件:", [heapq.heappop(mail)[2] for _ in range(4)])

# 键不是数字时(字符串)取不了相反数：用一个反转比较的包装类
class Rev:
    __slots__ = ("v",)
    def __init__(self, v): self.v = v
    def __lt__(self, other): return self.v > other.v      # 反过来比

words = ["pear", "apple", "zebra"]
h = [(Rev(w), w) for w in words]
heapq.heapify(h)
print("字符串大顶堆:", [heapq.heappop(h)[1] for _ in words])
# 也可以用 heapq.nlargest(k, items, key=...)：只要前 k 个时更省事
print("nlargest:", heapq.nlargest(2, words))
```

实际输出：

```
债权人(金额大的先): [(70, 'bob'), (70, 'cy'), (30, 'ann')]
紧急邮件: ['fire', 'flood', 'wind', 'low']
字符串大顶堆: ['zebra', 'pear', 'apple']
nlargest: ['zebra', 'pear']
```

**为什么。** 不用 `list.sort(reverse=True)`：它排一次，而堆的价值在于不断加入新元素的同时每次只取一个最大值，O(log n) 每次。

**易错。** 取反后别忘了取回：弹出的是 `-credit`，用的时候要还原。包装类必须保证 `__lt__` 和 `__eq__` 的行为一致，否则元组比较的「先看相等」会走错路。
