---
id: tlc-python-idioms-2-enumerate-zip
node: python.idioms
type: qa
step: 2
---
## Q
**Python 工具箱｜`enumerate`、`zip` 与矩阵转置**

同时要下标和值、并排遍历两个序列、转置或顺时针旋转矩阵，怎么写最简洁？`zip` 长度不一致会怎样？

## A
```python
for i, c in enumerate("abc", start=1):   # start 指定起始编号
    print(i, c, end=" ")                  # 1 a 2 b 3 c
m = [[1, 2, 3], [4, 5, 6]]
print([list(r) for r in zip(*m)])         # [[1,4],[2,5],[3,6]]：转置，*m 把每一行当作一个参数
print([list(r) for r in zip(*m[::-1])])   # [[4,1],[5,2],[6,3]]：先上下翻转再转置 = 顺时针旋转 90 度
print(list(zip("ab", [1, 2, 3])))         # [('a',1),('b',2)]：遇到最短的就停
```

- 比 `for i in range(len(a))` 少一层下标；LC 3 里 `for right, ch in enumerate(s)` 同时拿到右端点与字符。
- `zip(*m)` 转置；`zip(*m[::-1])` 顺时针转 90 度（LC 48）；`zip(*m)[::-1]` 之类要先 `list`。
- `zip(a, b, strict=True)`（3.10+）在长度不等时抛 `ValueError: zip() argument 2 is longer than argument 1`，用来提早暴露长度对不齐的 bug。
- `zip(*pairs)` 反过来「拆开」：`xs, ys = zip(*[(1, 'a'), (2, 'b')])` 得 `(1, 2)` 与 `('a', 'b')`。
- 并排遍历相邻元素用 `zip(a, a[1:])` 或 `itertools.pairwise`；三个序列同步遍历直接 `zip(a, b, c)`。
- **坑**：`zip` 返回迭代器，只能遍历一次；`zip(*m)` 在 `m` 为空时得到空，不会报错。
