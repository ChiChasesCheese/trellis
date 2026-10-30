---
id: uth-python-iterators-generators-3-generator-frame
node: python.iterators-generators
type: qa
step: 3
---
## Q
**生成器：函数怎么「暂停」**｜Python · CPython 3.14

带 `yield` 的函数为什么调用后不立刻执行？下一次 `next()` 又怎样从上次停下的地方继续？

## A
**背景。** 自己写迭代器类，要把状态（走到哪了、栈里还有什么）手工存进字段，很烦，中序遍历的迭代器就得自己维护一个栈。理想的写法是：写一个普通的循环，在需要「交出一个值」的地方暂停，之后原地接着跑，局部变量都还在。

**结构。** 生成器（generator）就是「暂停的函数调用」。调用带 `yield` 的函数时，函数体一行都不跑，只造出一个生成器对象，里面嵌着这次调用的栈帧（frame：局部变量、下一条要执行的指令位置、求值栈）。`next()` 把栈帧接回去跑到下一个 `yield`，交出值，栈帧随即冻结。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 235">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="15" y="15" width="195" height="170" rx="3"/>
<rect x="250" y="70" width="80" height="40" rx="3"/>
<line x1="212" y1="100" x2="250" y2="100"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="30" y="46" width="165" height="30" rx="3"/>
<rect x="30" y="86" width="165" height="30" rx="3"/>
<rect x="30" y="126" width="165" height="30" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="250" y1="82" x2="212" y2="82"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="250.0,100.0 244.0,103.0 244.0,97.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="212.0,82.0 218.0,79.0 218.0,85.0"/>
</g>
<g fill="currentColor">
<text x="112.5" y="65">局部变量 n = 3</text>
<text x="112.5" y="105">下一条: n += 1</text>
<text x="112.5" y="145">状态: SUSPENDED</text>
<text x="290" y="94">调用方</text>
<text x="170" y="210" font-size="11">CREATED  =&gt;  SUSPENDED  =&gt;  CLOSED</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="112" y="174" font-size="11">(栈帧嵌在对象里)</text>
<text x="231" y="116" font-size="11">yield n</text>
<text x="170" y="226" font-size="11">每次 yield 冻结, 每次 next 解冻</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="112" y="34">生成器对象 g = count()</text>
<text x="231" y="72" font-size="11">next</text>
</g>
</g>
</svg>
```

```python
def count():
    n = 0
    while True:
        yield n      # 暂停，交出 n
        n += 1       # 下次 next() 从这里继续
```

**细节。**

- `inspect.getgeneratorstate` 能看到状态：`GEN_CREATED`、`GEN_SUSPENDED`（停在某个 `yield`）、`GEN_CLOSED`（实测）。
- 栈帧直接嵌在生成器对象里；`for` 遍历生成器时被特化成 `FOR_ITER_GEN`，直接切进这个栈帧，不经过 `__next__` 的 C 调用。
- 函数里的 `return v` 变成 `StopIteration(v)`，`v` 放在异常的 `value` 里。

**为什么。** 比手写迭代器类短得多，状态由栈帧自动保存。

**例题：** LC 827 最大人工岛

给 `n x n` 的 0/1 网格，最多可以把一个 `0` 变成 `1`，求变完之后最大的岛屿面积（岛由上下左右相连的 `1` 组成）。`1 <= n <= 500`。例：`[[1,0],[0,1]]` 得 `3`，`[[1,1],[1,1]]` 得 `4`。

```python
from collections.abc import Iterator

def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    label = [[0] * n for _ in range(n)]            # 0 = 水或还没编号；岛从 1 开始编号
    size: dict[int, int] = {}                      # 岛编号 -> 面积

    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    def dfs(i: int, j: int, tag: int) -> int:      # 给这座岛的每一格打上 tag，返回面积
        label[i][j] = tag
        area = 1
        for a, b in neighbors(i, j):
            if grid[a][b] == 1 and label[a][b] == 0:
                area += dfs(a, b, tag)
        return area

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and label[i][j] == 0:
                tag = len(size) + 1
                size[tag] = dfs(i, j, tag)
    best = max(size.values(), default=0)           # 一格都不翻（或没有 0 可翻）
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                tags = {label[a][b] for a, b in neighbors(i, j)}   # 集合去重：同一座岛可能从几个方向碰到
                best = max(best, 1 + sum(size.get(t, 0) for t in tags))   # 水的编号是 0，不在 size 里，记 0
    return best
```
