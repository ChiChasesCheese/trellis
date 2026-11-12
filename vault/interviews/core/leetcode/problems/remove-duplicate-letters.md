---
slug: remove-duplicate-letters
---
## Q
**LC 316 去除重复字母**｜Medium

去掉 `s` 中的重复字母使每个字母只出现一次，不打乱相对顺序，求字典序最小的结果。

## A
**一句话。** 单调栈：当前字母比栈顶小且栈顶之后还会再出现，就弹掉栈顶；已在栈里的字母跳过。

```python
def remove_duplicate_letters(s):
    last = {ch: i for i, ch in enumerate(s)}   # 最后出现的下标
    stack = []
    in_stack = set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while (stack and stack[-1] > ch
               and last[stack[-1]] > i):
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（字母表大小 `26`）。

**易错点。**
- 弹栈不检查栈顶后面还会出现：`"bca"` 得 `"a"`，应为 `"bca"`。
- 不跳过已在栈里的字母：`"abab"` 得 `"aab"`，应为 `"ab"`。
- 直接 `sorted(set(s))`：`"bcab"` 得 `"abc"`，不是子序列，应为 `"bca"`。

**追问。**
- 要字典序最大？：弹栈条件改成 `stack[-1] < ch`。

**同模式。** LC 1081 不同字符的最小子序列、LC 402 移掉 K 位数字、LC 321 拼接最大数、LC 739 每日温度
