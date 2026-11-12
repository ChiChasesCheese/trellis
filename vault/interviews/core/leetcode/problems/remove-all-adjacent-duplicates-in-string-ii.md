---
slug: remove-all-adjacent-duplicates-in-string-ii
---
## Q
**LC 1209 删除字符串中的所有相邻重复项 II**｜Medium

反复删除字符串中 `k` 个相邻且相等的字母（删后两侧接拢），直到不能删，返回结果。

## A
**一句话。** 栈存 `(字符, 连续次数)`，与栈顶相同就计数加一，达到 `k` 整项弹出。

```python
def remove_duplicates(s, k):
    stack = []                       # (字符, 连续次数)
    for ch in s:
        if stack and stack[-1][0] == ch:
            _, cnt = stack.pop()
            if cnt + 1 < k:          # 凑够 k 就不放回
                stack.append((ch, cnt + 1))
        else:
            stack.append((ch, 1))
    return "".join(ch * cnt for ch, cnt in stack)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 一遍 `groupby` 每段保留 `len % k` 个：删后相邻段会合并成新的重复，`("deeedbbcccbdaa", 3)` 得 `'ddbbbdaa'`，应为 `'aa'`。
- 拼接时不乘计数：`("aaab", 4)` 得 `'ab'`，应为 `'aaab'`。

**追问。**
- 想省栈空间？：在 `list(s)` 上原地覆盖，写指针加计数数组，达到 `k` 时写指针回退 `k - 1` 位。

**同模式。** LC 1047 删除字符串中的所有相邻重复项、LC 2390 从字符串中移除星号、LC 735 小行星碰撞、LC 71 简化路径
