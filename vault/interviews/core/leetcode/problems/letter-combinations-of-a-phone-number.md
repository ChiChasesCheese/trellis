---
slug: letter-combinations-of-a-phone-number
---
## Q
**LC 17 电话号码的字母组合**｜Medium

给只含 `2-9` 的字符串 `digits`，按电话按键映射（`2` 对应 `abc`，`7` 对应 `pqrs` 等），返回所有字母组合。

## A
**一句话。** 回溯：`dfs(i)` 处理第 `i` 位，依次放入它的每个字母，递归后撤销。

```python
PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
         "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

def letter_combinations(digits):
    if not digits:
        return []                  # 不是 [""]
    ans, path = [], []

    def dfs(i):
        if i == len(digits):
            ans.append("".join(path))
            return
        for ch in PHONE[digits[i]]:
            path.append(ch)
            dfs(i + 1)
            path.pop()

    dfs(0)
    return ans
```

**复杂度。** 时间 `O(n·4^n)`，空间 `O(n)`。

**易错点。**
- 忘了 `path.pop()`：`"2"` 得 `['a','ab','abc']`，应为 `['a','b','c']`。
- 收集时 `ans.append(path)` 不 `join`：所有结果指向同一个列表，最后被清空。
- 空串返回 `[""]`：应为 `[]`。

**追问。**
- 不想递归？：`ans = [""]`，每个数字做 `[p + ch for p in ans for ch in PHONE[d]]`。
- 结果必须是词典里的词？：词典建 Trie，回溯时沿 Trie 走，没有前缀就剪枝。

**同模式。** LC 22 括号生成、LC 78 子集、LC 46 全排列、LC 39 组合总和
