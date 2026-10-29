---
id: tlc-letter-case-permutation-2-code
node: a.letter-case-permutation
type: qa
step: 2
---
## Q
**LC 784 字母大小写全排列**｜写出 Python 实现

字符串 `s`（长度 1 到 12，只含大小写字母和数字）里每个字母可以取大写或小写，返回所有能得到的字符串，顺序任意。

## A
**思路。** 按位置回溯：每一位先「保持原样」往下走；若是字母，再翻转大小写走第二支，回来后还原。走到末尾把当前字符列表拼成字符串收集。

```python
def letter_case_permutation(s: str) -> list[str]:
    res: list[str] = []
    path = list(s)                      # 原地改字符，回溯时改回来

    def dfs(i: int) -> None:
        if i == len(path):
            res.append("".join(path))
            return
        dfs(i + 1)                      # 这一位保持原样
        if path[i].isalpha():           # 只有字母才有第二个分支
            path[i] = path[i].swapcase()
            dfs(i + 1)
            path[i] = path[i].swapcase()   # 回溯：还原

    dfs(0)
    return res
```

运行：`"a1b2"` → `['a1b2', 'a1B2', 'A1b2', 'A1B2']`，`"3z4"` → `['3z4', '3Z4']`，`"12"` → `['12']`，`"aB"` → `['aB', 'ab', 'AB', 'Ab']`。

**复杂度。** 时间 `O(2^m · n)`，`m` 为字母个数：`2^m` 个叶子，每个 `join` 是 `O(n)`；除输出外空间 `O(n)`，递归深度至多 12。

**写法要点。** 字符串不可变，所以转成 `list` 原地改，叶子处才 `"".join` 生成新串；`swapcase()` 一步完成大小写翻转，不用判断原来是大写还是小写；内层函数直接读写外层的 `res`、`path`（只改内容、不重新绑定，不需要 `nonlocal`）。
