---
slug: decode-string
---
## Q
**LC 394 字符串解码**｜Medium

解码 `k[encoded]`（括号内重复 `k` 次，可嵌套，`k` 可为多位数），如 `"3[a2[c]]"` → `"accaccacc"`。

## A
**一句话。** 栈保存外层状态：遇 `[` 压入（前缀、次数）并清空当前层，遇 `]` 弹出并把当前层重复后接在前缀后。

```python
def decode_string(s):
    stack = []                   # (进入 [ 前的前缀, 重复次数)
    cur, num = "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)   # 次数可能多位
        elif ch == "[":
            stack.append((cur, num))
            cur, num = "", 0           # 新的一层
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times
        else:
            cur += ch
    return cur
```

**复杂度。** 时间 `O(输出长度)`，空间 `O(输出长度)`。

**易错点。**
- 次数写成 `num = int(ch)`：`"10[a]"` 得空串，应为十个 `a`。
- 前缀没压栈：`"ab2[c]"` 得 `"cc"`，应为 `"abcc"`。
- 进 `[` 后没清零 `num`：`"3[a]2[bc]"` 的 `2` 接成 `32`。

**追问。**
- 只要第 `k` 个字符（LC 880）？：不展开，从后往前按长度反推。
- 输出会爆炸怎么办？：只算长度，或做成生成器按需产出。

**同模式。** LC 224 基本计算器、LC 227 基本计算器 II、LC 726 原子的数量、LC 20 有效的括号
