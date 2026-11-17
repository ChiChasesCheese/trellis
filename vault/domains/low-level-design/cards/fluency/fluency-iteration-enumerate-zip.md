---
id: fluency-iteration-enumerate-zip
node: fluency.iteration
type: qa
step: 3
---
## Q
同时遍历 `names` 和 `scores` 两个列表，有人写 `for i in range(len(names))`。`enumerate`、`zip` 怎么替换？两个列表长度不一样时 `zip` 会怎样，`itertools.groupby` 的前提是什么？

## A
**下标用 enumerate，并行用 zip，分组先排序**

- **`enumerate(xs, start=1)`**：同时给出序号和元素，不用手写 `range(len(...))` 和下标取值；序号从 1 开始用 `start=1`；
- **`zip(a, b)`**：并行遍历；长度不同时按最短的截断，**悄悄丢掉**多出来的元素；两个列表本应一一对应时用 `zip(a, b, strict=True)`（3.10 起），长度不等抛 `ValueError`；
- **解包**：`for key, value in d.items()`、`first, *rest = xs`、`for (x, y), z in …`；比下标取值自解释；
- **`itertools.groupby` 只合并相邻的相同键**：数据没按键排序，同一个键会出现多段；先 `sorted(data, key=…)` 再分组；并且每一组是迭代器，要在移动到下一组之前用掉（`list(g)`）；
- **何时不用**：只要一个字典的汇总，`defaultdict(list)` 一遍遍历就够，不需要先排序。

```python
from itertools import groupby

names, scores = ["a", "b", "c"], [1, 2]
print(list(zip(names, scores)))                  # [('a', 1), ('b', 2)]：c 被丢掉
try: list(zip(names, scores, strict=True))
except ValueError as e: print(e)                 # zip() argument 2 is shorter than argument 1
print(list(enumerate(names, start=1)))          # [(1, 'a'), (2, 'b'), (3, 'c')]

data = ["a1", "b1", "a2"]
print([(k, list(g)) for k, g in groupby(data, key=lambda s: s[0])])          # a 出现两段
print([(k, list(g)) for k, g in groupby(sorted(data), key=lambda s: s[0])])  # 先排序才合并
```

**知识点：**迭代写法（Iteration Style）
