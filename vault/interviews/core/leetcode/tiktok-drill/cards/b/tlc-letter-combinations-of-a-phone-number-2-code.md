---
id: tlc-letter-combinations-of-a-phone-number-2-code
node: b.letter-combinations-of-a-phone-number
type: qa
step: 2
---
## Q
**LC 17 电话号码的字母组合**｜写出 Python 实现

给只含数字 `2-9` 的字符串 `digits`（长度 `1` 到 `4`），按电话按键映射（`2`→`abc`、`3`→`def`、`4`→`ghi`、`5`→`jkl`、`6`→`mno`、`7`→`pqrs`、`8`→`tuv`、`9`→`wxyz`）返回所有字母组合，顺序不限。

## A
**思路。** 回溯：`dfs(i)` 处理第 `i` 个数字，对它的每个字母，放入共享路径 `path`，递归下一位，再弹出；`i` 等于长度时把路径拼成字符串。

```python
PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
         "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def letter_combinations(digits: str) -> list[str]:
    if not digits:                         # 空输入没有任何组合，返回 []（不是 [""]）
        return []
    ans: list[str] = []
    path: list[str] = []                   # 当前已选的字母，长度 == 当前处理到的位数

    def dfs(i: int) -> None:
        if i == len(digits):
            ans.append("".join(path))
            return
        for ch in PHONE[digits[i]]:
            path.append(ch)
            dfs(i + 1)
            path.pop()                     # 回溯：撤销选择

    dfs(0)
    return ans
```

运行：`"23"` → `['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']`；`"2"` → `['a', 'b', 'c']`；`""` → `[]`；`"7979"` 产生 `256` 个组合。

**复杂度。** 时间 `O(n · 4^n)`：叶子最多 `4^n` 个，每个 `join` 花 `O(n)`；空间 `O(n)`（递归栈与 `path`，不含输出）。

**写法要点。** 映射表用 `dict[str, str]`，值是字符串，可以直接 `for ch in ...` 遍历；闭包 `dfs` 直接读写外层的 `ans` 和 `path`（只改内容、不重新绑定，所以不需要 `nonlocal`）；`path` 用列表而不是字符串拼接，`append` / `pop` 是 `O(1)`，字符串每次拼接都会复制。
