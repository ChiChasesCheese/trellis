---
id: tlc-python-itertools-functools-5-chain-islice
node: python.itertools-functools
type: qa
step: 5
---
## Q
**Python 工具箱｜`chain`、`islice`、`zip_longest`、`takewhile`**

把多个序列接在一起、只取迭代器的一段、两个长度不同的序列配对，各自用哪个函数？

## A
```python
from itertools import chain, islice, count, zip_longest, takewhile, dropwhile
print(list(chain([1, 2], (3,), "ab")))              # [1, 2, 3, 'a', 'b']
print(list(chain.from_iterable([[1], [2, 3], []]))) # [1, 2, 3]：展平一层
print(list(islice(range(100), 3, 10, 3)))           # [3, 6, 9]：切片，不复制
print(list(zip_longest([1, 2, 3], [1], fillvalue=0)))   # [(1,1),(2,0),(3,0)]
print(list(takewhile(lambda x: x < 3, [1, 2, 3, 1])), list(dropwhile(lambda x: x < 3, [1, 2, 3, 1])))
# [1, 2] [3, 1]
```

- `chain(a, b)` 不拷贝；遍历两个列表用 `for x in chain(a, b)`，比 `a + b` 省一次拷贝。`chain.from_iterable(rows)` 把二维展平，例如 `max(chain.from_iterable(grid))` 取矩阵最大值。
- `islice(it, start, stop, step)` 对**迭代器**切片，不能用负数；用来取生成器的前 `k` 个，如 `list(islice(gen, k))`。
- `zip_longest` 处理两个数字链表逐位相加（LC 2、415 加字符串）：把短的补 0。
- `zip` 遇到最短就停；3.10+ 的 `zip(a, b, strict=True)` 在长度不等时抛 `ValueError`，用来暴露长度不一致的 bug。
- **坑**：`takewhile` 会**多消耗一个**不满足条件的元素；之后用同一个迭代器继续读，会丢掉那一个。
