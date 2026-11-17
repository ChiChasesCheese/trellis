---
id: reading-predict-aliasing
node: reading.predict-behaviour
type: qa
step: 1
---
## Q
下面这段代码最后打印什么？不运行，怎么推演出来？

```python
grid = [[0] * 2] * 2
grid[0][0] = 1
a = [1, 2]; b = a; b.append(3)
print(grid, a)
```

## A
**推演靠“名字指向哪个对象”，不是看值：`[[0]*2]*2` 里两行是同一个列表**

- **赋值不复制**：`b = a` 让两个名字指向同一个列表，改 `b` 就是改 `a`；
- **乘法复制的是引用**：`[x] * 2` 得到两个指向同一个 `x` 的元素；内层是可变列表，两行就共用；
- **所以 `grid[0][0] = 1` 改的是同一行**：两行同时变，输出 `[[1, 0], [1, 0]]`；`a` 被 `b.append` 改成 `[1, 2, 3]`；
- **推演方法**：给每个对象编号（#1、#2），写出每个名字指向哪个编号，每步更新这张表；看到“改一个、变两个”就是别名；
- **想要独立的行**：用推导式 `[[0] * 2 for _ in range(2)]`，每次循环新建一个列表。

```python
grid = [[0] * 2] * 2
print(grid[0] is grid[1])           # True：两行是同一个对象
a = [1, 2]; b = a
print(b is a)                       # True：b 只是 a 的另一个名字
ok = [[0] * 2 for _ in range(2)]
ok[0][0] = 1
print(ok)                           # [[1, 0], [0, 0]]：各行独立
```

**知识点：**预测输出与副作用（Predicting Behaviour）
