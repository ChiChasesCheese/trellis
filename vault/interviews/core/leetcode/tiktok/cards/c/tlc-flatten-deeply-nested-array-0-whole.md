---
id: tlc-flatten-deeply-nested-array-0-whole
node: c.flatten-deeply-nested-array
type: qa
---
## Q
**LC 2625 扁平化嵌套数组**｜Medium · LC TikTok 全时段热度 38/100

原题是 JavaScript 题；这里用 Python 的嵌套 `list` 解同一任务，不使用任何内置展开方法。给定多维数组 `arr`（元素是整数或其他多维数组）和深度 `n`，返回扁平化后的数组：只有嵌套深度小于 `n` 的子数组才被展开，第一层数组中元素的深度为 `0`。`0 <= arr 的元素个数 <= 10^5`，`0 <= arr 的子数组个数 <= 10^5`，最大嵌套深度 `<= 1000`，`-1000 <= 整数 <= 1000`，`0 <= n <= 1000`。例：`arr = [1,2,3,[4,5,6],[7,8,[9,10,11],12],[13,14,15]]`，`n = 0` → 原数组；`n = 1` → `[1,2,3,4,5,6,7,8,[9,10,11],12,13,14,15]`；`arr = [[1,2,3],[4,5,6],[7,8,[9,10,11],12],[13,14,15]]`，`n = 2` → `[1,2,...,15]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归遍历：遇到子数组且「展开预算」`n > 0` 就带着 `n - 1` 递归展开，否则原样保留。

**识别。** 「嵌套结构按深度展开」是递归；把「深度 < n」换成「剩余预算 n 递减」，判断变成 `n > 0`，不用单独传深度。

**推导。** 暴力：循环 `n` 次，每次把所有一层子数组展开一遍，`O(n * 元素数)`。洞察：一次遍历就能完成，每个元素只访问一次；子数组每深入一层把预算减 1，预算归零就不再展开。

```python
def flatten(arr: list, n: int) -> list:
    out: list = []
    for item in arr:
        if isinstance(item, list) and n > 0:     # 深度 < n 的子数组才展开，每深入一层预算减 1
            out.extend(flatten(item, n - 1))
        else:                                    # 整数，或预算用完的子数组：原样保留
            out.append(item)
    return out
```

运行：三个示例依次得到原数组、`[1,2,3,4,5,6,7,8,[9,10,11],12,13,14,15]`、`[1,2,...,15]`；`flatten([], 5)` → `[]`；嵌套 1500 层、`n = 2000` 时递归版抛出 `RecursionError`。

**复杂度。** 时间 `O(总元素数)`（每个元素访问一次，`extend` 总拷贝量与展开层数相关，最坏 `O(元素数 * 深度)`），空间 `O(深度)`。

**拓展优化。**
- 深度达 1000 时递归版接近 CPython 默认上限，改成迭代器栈：栈里每层是一个迭代器，`len(stack) - 1` 即当前深度，完全不受递归限制：

```python
def flatten_iterative(arr: list, n: int) -> list:
    out: list = []
    stack = [iter(arr)]                          # 栈里每一层是一个迭代器，len(stack)-1 就是当前元素的深度
    while stack:
        for item in stack[-1]:
            if isinstance(item, list) and len(stack) <= n:   # 深度 len(stack)-1 < n 才展开
                stack.append(iter(item))
                break                            # 先处理子数组，处理完回来继续迭代器剩余部分
            out.append(item)
        else:
            stack.pop()                          # 这一层迭代完毕
    return out
```

- 返回生成器（`yield from`）可以惰性展开，不一次性构造大列表。

**易错点。**
- 把 `n > 0` 写成 `n >= 0`：多展开一层，示例一 `n = 0` 会被展开。
- 用 `type(x) == list` 或 `hasattr` 判断：用 `isinstance(item, list)`；整数没有 `extend`，不能对它递归。
- 最坏深度：嵌套 1000 层的数组递归深度约 1000，CPython 默认限制约 1000，会 `RecursionError`；需要 `sys.setrecursionlimit` 或改成迭代版。

**追问。**
- 不限定深度（完全展开）：`n = float("inf")` 即可，或去掉预算判断。
- 改为生成器 `yield from`：返回迭代器，内存 `O(深度)`。

**同模式。** LC 341 扁平化嵌套列表迭代器、LC 385 迷你语法分析器、LC 339 嵌套列表权重和、LC 388 文件的最长绝对路径、LC 394 字符串解码。
