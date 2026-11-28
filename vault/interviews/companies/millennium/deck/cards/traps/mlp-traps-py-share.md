---
id: mlp-traps-py-share
node: traps.python-output
type: qa
step: 2
---
## Q
**列表乘法与生成器**｜语言陷阱与读代码

下面的 Python 代码输出什么？

```python
grid = [[0] * 2] * 2
grid[0][0] = 1
print(grid)
g = (n * n for n in range(3))
print(list(g), list(g))
```

## A
**输出。**
```
[[1, 0], [1, 0]]
[0, 1, 4] []
```

- **`[[0] * 2] * 2`：** 外层乘法把同一个内层列表复制了两次引用，两行其实是同一个对象；改 `grid[0][0]` 等于改了两行。
- **内层 `[0] * 2` 没问题：** 整数不可变，两个 0 互不影响；问题只在元素本身是可变对象时。
- **修法：** 用推导式 `[[0] * 2 for _ in range(2)]`，每次循环新建一个内层列表；这时 `grid[0][0] = 1` 得 `[[1, 0], [0, 0]]`。
- **生成器只能遍历一次：** 第一个 `list(g)` 把值取光，第二个 `list(g)` 得到空列表，不报错；需要多次遍历就存成列表，或每次重新创建生成器。
- **记住：** 乘法复制的是引用，不是对象；生成器用完即空。二维表一律用推导式。

**英文答法。**
- "The multiplication copies the **reference**, so all rows are the same list."
- "A generator is **exhausted** after one pass; I'd materialize it with `list` if I need it twice."
