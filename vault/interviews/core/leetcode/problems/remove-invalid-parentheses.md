---
slug: remove-invalid-parentheses
---
## Q
**LC 301 删除无效的括号**｜Hard

删除最少数量的括号，使字符串有效，返回所有不重复的结果。

## A
**一句话。** 先扫一趟算出必须删的左、右括号数，再回溯对每个括号选删或留，用剩余额度和未配对数剪枝，集合去重。

```python
def remove_invalid_parentheses(s):
    left_rem = right_rem = 0     # 必须删的 ( 和 ) 数
    for ch in s:
        if ch == "(":
            left_rem += 1
        elif ch == ")":
            if left_rem:
                left_rem -= 1    # 配上一个 (
            else:
                right_rem += 1   # 无 ( 可配，必须删
    delta = {"(": 1, ")": -1}
    res, path = set(), []        # 集合去重
    def dfs(i, left, right, bal):
        if (left < 0 or right < 0 or bal < 0
                or left + right > len(s) - i):
            return               # 删多了、) 超前、字符不够删
        if i == len(s):
            if left == right == bal == 0:
                res.add("".join(path))
            return
        ch = s[i]
        if ch == "(":
            dfs(i + 1, left - 1, right, bal)    # 删这个 (
        elif ch == ")":
            dfs(i + 1, left, right - 1, bal)    # 删这个 )
        path.append(ch)                         # 保留
        dfs(i + 1, left, right, bal + delta.get(ch, 0))
        path.pop()
    dfs(0, left_rem, right_rem, 0)
    return list(res)
```

**复杂度。** 时间 `O(2^k·n)`（`k` 为括号数，剪枝后远小），空间 `O(n)`。

**易错点。**
- 结果用列表：`"()())()"` 删第 4 个或第 5 个 `)` 得同一串，要去重。
- 不限制删除额度：混进更短的有效串如 `"()"`，违反「最少」。
- 漏了「字符不够删」的剪枝：`"("*20` 要展开上百万次调用。

**追问。**
- 只要最少删除数？：扫描得到的 `left_rem + right_rem` 就是，`O(n)`。
- 括号有多种？：`bal` 不够用，要换成栈。

**同模式。** LC 20 有效的括号、LC 22 括号生成、LC 921 使括号有效的最少添加、LC 1249 移除无效的括号
