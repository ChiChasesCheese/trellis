---
slug: remove-all-occurrences-of-a-substring
---
## Q
**LC 1910 删除一个字符串中所有出现的给定子字符串**｜Medium

反复删除 `s` 中最左边出现的 `part`，直到不再出现，返回剩下的字符串。

## A
**一句话。** 用栈逐字符压入，栈顶一旦拼出 `part` 就整段弹掉，删除后新接上的部分自然会被继续检查。

```python
def remove_occurrences(s, part):
    st, k = [], len(part)
    for c in s:
        st.append(c)
        # 栈顶拼出 part 就整段弹掉，新暴露的前缀还能再拼
        if len(st) >= k and "".join(st[-k:]) == part:
            del st[-k:]
    return "".join(st)
```

**复杂度。** 时间 `O(n·m)`，`m = len(part)`；空间 `O(n)`。

**易错点。**
- 只扫一遍 `replace`：删掉一段后两边拼起来会出现新的 `part`，如 `"daabcbaabcbc"` 要删三次。
- 只在压入时比较最后一个字符：必须比较整个栈顶 `k` 个字符。

**追问。**
- 为什么栈的结果等于「每次删最左边」？：栈按从左到右的顺序在第一时间删掉最早完成的那次出现，与反复删最左的结果相同。
- `part` 很长要更快？：栈里同时存 KMP 的匹配长度，每压入一个字符 `O(1)` 均摊更新，总 `O(n + m)`。

**同模式。** LC 20 有效的括号、LC 1047 删除字符串中的所有相邻重复项、LC 1209 删除字符串中的所有相邻重复项 II、LC 2390 从字符串中移除星号
