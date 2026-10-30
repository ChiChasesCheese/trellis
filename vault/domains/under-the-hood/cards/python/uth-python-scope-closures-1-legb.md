---
id: uth-python-scope-closures-1-legb
node: python.scope-closures
type: qa
step: 1
---
## Q
**函数里用到的名字去哪找**｜Python · CPython 3.14

嵌套函数 `dfs` 里同时用到 `len`、`path`、`i`，Python 怎么知道它们各自指什么？

## A
**背景。** 同一个名字在不同函数里可以指不同的东西，递归时每一层还各有一份局部变量。如果所有名字挤在一张全局表里，就会互相覆盖。办法是名字分层：每次函数调用有自己的一层，本层没有，再往外一层找。

**结构。** 查找顺序是 LEGB：局部（Local，当前函数）→ 外层函数（Enclosing）→ 全局（Global，本模块）→ 内置（Built-in，如 `len`）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="6" y="6" width="328" height="206" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="24" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B 内置  len  enumerate</text>
<rect x="18" y="40" width="304" height="164" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">G 全局  permute</text>
<rect x="30" y="74" width="280" height="122" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">E 外层  nums n res path used</text>
<rect x="42" y="108" width="256" height="80" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="50" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">L 局部  i  x</text>
<text x="50" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dfs 里的 i x 在 L  path 在 E</text>
<text x="50" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">len 在 B  由内向外逐层找</text>
<text x="170" y="238" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">都找不到就是 NameError</text>
</svg>
```

**细节。**

- 名字在哪一层，编译时就定了，不是运行时一层层试。
- `dfs` 编译出的字节码：`i`、`x` 走 `LOAD_FAST` 一族指令，`path`、`n` 走 `LOAD_DEREF`，`len`、`enumerate` 走 `LOAD_GLOBAL`。
- 函数、类体、模块各有一层；`if`、`for` 不产生新一层，循环变量在循环结束后依然存在。
- 四层都找不到：`NameError`。

**为什么。** 分层让同名变量互不干扰，嵌套函数又能直接读外层变量，不用一路传参。

**例题：** LC 46 全排列

给一个不含重复数字的数组 `nums`，返回它所有可能的全排列，顺序不限。`1 <= nums.length <= 6`。例：`[1,2,3]` 得 `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`。

```python
def permute(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    res: list[list[int]] = []
    path: list[int] = []                # 当前已选出的前缀
    used = [False] * n                  # used[i]：nums[i] 是否已在 path 里

    def dfs() -> None:
        if len(path) == n:
            res.append(path[:])         # 必须拷贝，path 之后还会被改
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()                  # 撤销选择，回到上一层的状态
            used[i] = False

    dfs()
    return res
```
