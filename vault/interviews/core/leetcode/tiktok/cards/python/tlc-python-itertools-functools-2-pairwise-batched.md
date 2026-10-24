---
id: tlc-python-itertools-functools-2-pairwise-batched
node: python.itertools-functools
type: qa
step: 2
---
## Q
**Python 工具箱｜`pairwise` 与 `batched`**

「相邻两项」和「每 k 个一组」怎样不用下标地写？网格四个方向的偏移量有什么地道写法？

## A
`pairwise(it)`（3.10+）产出 `(x0,x1), (x1,x2), ...`，相邻对；`batched(it, n)`（3.12+）产出长度 `n` 的元组，最后一组可能更短。

```python
from itertools import pairwise, batched
print([b - a for a, b in pairwise([1, 4, 9, 16])])   # [3, 5, 7]：相邻差
print(list(batched(range(7), 3)))                    # [(0,1,2), (3,4,5), (6,)]
dirs = (0, 1, 0, -1, 0)
print(list(pairwise(dirs)))                          # [(0,1), (1,0), (0,-1), (-1,0)]：四个方向
```

- 比 `zip(a, a[1:])` 好：不复制切片，输入可以是任意迭代器（生成器、文件）。
- 相邻比较类：是否严格递增 `all(a < b for a, b in pairwise(nums))`；最长山脉（LC 845）里判断上坡 / 下坡；相邻元素之差。
- 网格四邻域的常用写法是 `for dr, dc in pairwise((0, 1, 0, -1, 0)):`，比手写四个元组更短、不容易写错符号。
- `batched` 用于分批处理输入（每 k 个一组）；3.12 之前要自己写。
- **坑**：`pairwise` 对长度不足 2 的输入产出空；`batched(it, 0)` 抛 `ValueError`。
