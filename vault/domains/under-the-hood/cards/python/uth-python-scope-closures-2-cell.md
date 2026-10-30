---
id: uth-python-scope-closures-2-cell
node: python.scope-closures
type: qa
step: 2
---
## Q
**外层返回后，内层怎么还记得它的变量**｜Python · CPython 3.14

`make_counter()` 已经返回了，它的局部变量 `n` 按理该随栈帧销毁，为什么内层的 `inc()` 还能读写 `n`？

## A
**背景。** 普通局部变量放在函数的栈帧（frame，一次调用的工作区）里，函数一返回，栈帧就销毁。可内层函数要在外层返回之后继续用 `n`，所以 `n` 不能只放在栈帧里。

**结构。** 编译器发现 `n` 被内层函数用到，就把它放进一个单独的小对象：cell（单元格，里面只有一个指针）。外层和内层函数各自持有这个 cell，改的是 cell 里的指针，所以彼此看得见。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<rect x="10" y="40" width="120" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="70" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">make_counter</text>
<text x="70" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">栈帧 已销毁</text>
<rect x="170" y="40" width="70" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="205" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cell</text>
<rect x="270" y="40" width="46" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="293" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">int 1</text>
<line x1="240" y1="56" x2="268" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268.0,56.0 262.0,59.0 262.0,53.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="138" width="110" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="205" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">inc 函数</text>
<line x1="205" y1="138" x2="205" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="205.0,74.0 208.0,80.0 202.0,80.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="214" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">__closure__</text>
<line x1="130" y1="56" x2="168" y2="56" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="170" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">外层返回后 cell 仍被 inc 引用</text>
</svg>
```

**细节。**

- 内层函数对象的 `__closure__` 是一个 cell 元组；`inc.__closure__[0].cell_contents` 读出 `n` 当前的值。
- 外层函数自己也通过 cell 读写 `n`，字节码是 `LOAD_DEREF` 和 `STORE_DEREF`。
- 内层 `def` 执行时，才把这个 cell 元组装进新建的函数对象。

**为什么。** 共享的是变量（cell）而不是值：外层之后再改 `n`，内层读到的就是新值。

**例题：** LC 200 岛屿数量

给由字符 `'1'`（陆地）和 `'0'`（水）组成的二维网格，陆地只按上下左右相连成岛，求岛屿总数。`1 <= m, n <= 300`。

```python
def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return                                      # 出界或水：这条搜索到头
        grid[r][c] = "0"                                # 先沉掉再往四周搜，同一格不会被重复进入
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1                              # 找到一座新岛：把它整座沉掉
                sink(r, c)
    return count
```
