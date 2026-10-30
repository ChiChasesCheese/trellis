---
id: tlc-remove-invalid-parentheses-2-code
node: b.remove-invalid-parentheses
type: qa
step: 2
---
## Q
**LC 301 删除无效的括号**｜写出 Python 实现

字符串 `s`（长度 `1` 到 `25`，只含小写字母和圆括号，括号至多 `20` 个）。删除最少数量的括号使其有效，返回所有不同的结果，顺序任意。

## A
**思路。** 先扫描算出最少要删的左括号数 `left_rem` 和右括号数 `right_rem`。再用 DFS 逐字符决定：括号可以删（对应额度减一）或保留（更新 `balance`），字母必须保留。违反额度或 `balance < 0` 就剪枝；走到末尾且额度和 `balance` 都为零时，把拼出的串放进集合。

```python
def remove_invalid_parentheses(s: str) -> list[str]:
    left_rem = right_rem = 0                   # 至少还要删多少个 ( 和 )
    for ch in s:
        if ch == "(":
            left_rem += 1
        elif ch == ")":
            if left_rem:
                left_rem -= 1                  # 这个 ) 能和前面某个 ( 配对
            else:
                right_rem += 1                 # 前面没有可配的 (，这个 ) 必须删
    delta = {"(": 1, ")": -1}
    res: set[str] = set()                      # 不同位置删同样的括号会得到同一个串，用集合去重
    path: list[str] = []

    def dfs(i: int, left: int, right: int, balance: int) -> None:
        if left < 0 or right < 0 or balance < 0 or left + right > len(s) - i:
            return                             # 删多了、) 已无法挽回、或剩下的字符不够删
        if i == len(s):
            if left == right == balance == 0:
                res.add("".join(path))
            return
        ch = s[i]
        if ch == "(":
            dfs(i + 1, left - 1, right, balance)       # 删掉这个 (
        elif ch == ")":
            dfs(i + 1, left, right - 1, balance)       # 删掉这个 )
        path.append(ch)                                # 保留这个字符
        dfs(i + 1, left, right, balance + delta.get(ch, 0))
        path.pop()

    dfs(0, left_rem, right_rem, 0)
    return list(res)
```

运行（结果排序后）：`"()())()"` → `['(())()', '()()()']`，`"(a)())()"` → `['(a())()', '(a)()()']`，`")("` → `['']`，`"((("` → `['']`，`")))()"` → `['()']`，`"a"` → `['a']`。

**复杂度。** 时间最坏 `O(2^k · n)`，`k <= 20` 是括号个数，预算剪枝让实际搜索量小得多；空间 `O(n)`（递归深度 + `path`），不含结果。

**写法要点。** `left == right == balance == 0` 链式比较一次判三个量；`delta.get(ch, 0)` 让字母的 `balance` 增量为 `0`，省掉 `if` 分支；`path` 用列表 `append/pop` 做回溯，比字符串拼接少拷贝；`set[str]` 去重后再 `list()`；`left + right > len(s) - i` 是「剩下的字符都删掉也凑不够额度」的剪枝，没有它 `"(" * 20` 会展开约 `2 · 10^6` 次调用。
