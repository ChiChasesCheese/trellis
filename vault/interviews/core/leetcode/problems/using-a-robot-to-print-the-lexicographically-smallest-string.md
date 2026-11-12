---
slug: using-a-robot-to-print-the-lexicographically-smallest-string
---
## Q
**LC 2434 使用机器人打印字典序最小的字符串**｜Medium

字符串 `s` 的首字符可压入栈 `t`，也可弹出 `t` 的栈顶写到纸上。直到两者都空，返回纸上字典序最小的字符串。

## A
**一句话。** 栈加后缀最小值的贪心：栈顶不大于 `s` 剩余部分的最小字符时就写出。

```python
def robot_with_string(s):
    n = len(s)
    suf = ["{"] * (n + 1)      # suf[i]=min(s[i:])，'{'>'z'
    for i in range(n - 1, -1, -1):
        suf[i] = min(s[i], suf[i + 1])
    paper, t = [], []
    for i, ch in enumerate(s):
        t.append(ch)
        while t and t[-1] <= suf[i + 1]:
            paper.append(t.pop())
    return "".join(paper)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只和 `s[i+1]` 比而不是整个后缀最小值：`"bdda"` 得 `"bdad"`，应为 `"addb"`。
- 哨兵不够大：换成 `"a"`，`"zza"` 只写出 `"a"`，栈里的 `z` 弹不出，应为 `"azz"`。

**追问。**
- 为什么等于时也要弹出？：栈顶与后缀最小值相等时，先写出不会更差，且避免后面被压住。
- 为什么是贪心？：栈顶已是能写的最小字符时再等只会让更大的字符先出。

**同模式。** LC 402 移掉 K 位数字、LC 316 去除重复字母、LC 946 验证栈序列、LC 155 最小栈
