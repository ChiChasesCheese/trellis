---
id: tlc-letter-case-permutation-0-whole
node: b.letter-case-permutation
type: qa
---
## Q
**LC 784 字母大小写全排列**｜Easy · CodeTop 国内累计 2 次 · 最近 2026-03-14（国内 CodeTop）

给字符串 `s`，把其中每个字母任意变成大写或小写（数字不变），返回能得到的**所有**字符串，顺序任意。`1 <= s.length <= 12`，`s` 只含大小写英文字母和数字。例：`"a1b2"` → `["a1b2","a1B2","A1b2","A1B2"]`，`"3z4"` → `["3z4","3Z4"]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每个字母是一个「保持 / 翻转大小写」的二选一，数字只有一个选项；按位置做回溯（backtracking），走到末尾就收集一个结果，共 `2^m` 个（`m` 为字母个数）。

**识别。** 「返回**所有**可能的字符串」是枚举信号，输出本身有 `2^m` 个，不存在比输出规模更快的算法；`n <= 12` 说明指数级是预期的。每一位的选择互相独立，所以决策树是一棵按位置展开的二叉树（数字处只有一个分支），即各位选项的笛卡尔积（Cartesian product）。

**推导。** 暴力：对全部 `n` 位枚举 `2^n` 个大小写掩码，再用集合去重；数字位的两个「分支」生成同一个字符串，白做了一半又一半。洞察：只在字母处分叉，数字直接往下走，结果天然互不相同，无需去重。实现上用一个可变的字符列表 `path` 原地修改，进入分支前翻转、回来后还原，每个结果只在叶子处 `join` 一次。

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

运行：`"a1b2"` → `['a1b2', 'a1B2', 'A1b2', 'A1B2']`，`"3z4"` → `['3z4', '3Z4']`，`"12"` → `['12']`，`"aB"` → `['aB', 'ab', 'AB', 'Ab']`；`"a" * 12` 得到 `4096` 个结果。

**复杂度。** 时间 `O(2^m · n)`：`2^m` 个叶子，每个 `join` 花 `O(n)`；除输出外空间 `O(n)`（递归深度和 `path`）。

**易错点。**
- 数字位也分两支（`lower()` / `upper()` 各走一次）：数字的大小写相同，结果重复。`"3z4"` 会得到 8 个字符串（`'3z4'`、`'3Z4'` 各 4 次），正确是 2 个。
- 在叶子处 `res.append(path)` 而不是 `"".join(path)`：存的是同一个列表的引用，回溯结束后全部变成同一个值。
**追问。**
- 不用递归：`itertools.product(*[(c.lower(), c.upper()) if c.isalpha() else (c,) for c in s])`，每个元组 `join` 一次。
- 只要个数：`2 ** sum(c.isalpha() for c in s)`，`O(n)`。
- 要求字典序输出：Python 中大写字母小于小写，对结果 `sorted()` 即可，`O(2^m · n · m)`。

**同模式。** LC 78 子集、LC 17 电话号码的字母组合、LC 22 括号生成、LC 1239 串联字符串的最大长度。
