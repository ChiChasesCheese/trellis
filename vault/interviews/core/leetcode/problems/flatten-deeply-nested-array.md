---
slug: flatten-deeply-nested-array
---
## Q
**LC 2625 扁平化嵌套数组**｜Medium

（原题为 JavaScript，这里用 Python 嵌套 `list`。）把多维数组 `arr` 展开到深度 `n`：只有深度小于 `n` 的子数组才展开（第一层元素深度为 `0`）。

## A
**一句话。** 递归遍历：遇到子数组且预算 `n > 0` 就带 `n - 1` 递归展开，否则原样保留。

```python
def flatten(arr, n):
    out = []
    for item in arr:
        if isinstance(item, list) and n > 0:
            out.extend(flatten(item, n - 1))
        else:                  # 整数，或预算用完的子数组
            out.append(item)
    return out
```

**复杂度。** 时间 `O(总元素数 * 深度)`，空间 `O(深度)`。

**易错点。**
- `n > 0` 写成 `n >= 0`：多展开一层，`n=0` 时数组也被展开。
- 嵌套 1000 层：递归深度触顶，抛 `RecursionError`。

**追问。**
- 完全展开？：`n = float("inf")`。
- 想省内存？：用生成器 `yield from`，内存 `O(深度)`。

**同模式。** LC 341 扁平化嵌套列表迭代器、LC 385 迷你语法分析器、LC 339 嵌套列表权重和、LC 394 字符串解码
