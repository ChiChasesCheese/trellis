---
id: tlc-decode-string-2-code
node: a.decode-string
type: qa
step: 2
---
## Q
**LC 394 字符串解码**｜写出 Python 实现

合法的编码串 `s`（长度 `1` 到 `30`，由小写字母、数字和 `[]` 组成，次数在 `[1, 300]`，解码后长度不超过 `10^5`），`k[encoded]` 表示 `encoded` 重复 `k` 次，返回解码后的字符串。

## A
**思路。** 一遍扫描，变量 `cur` 是当前层已拼好的字符串，`num` 是正在读的次数。遇到 `[` 把 `(cur, num)` 压栈并清空；遇到 `]` 弹出 `(prev, times)`，令 `cur = prev + cur * times`。

```python
def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []     # (进入 [ 之前已拼好的前缀, 这一层的重复次数)
    cur, num = "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)      # 次数可能是多位数
        elif ch == "[":
            stack.append((cur, num))
            cur, num = "", 0              # 进入新的一层，从空串重新拼
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times      # 把这一层重复 times 次接到前缀后面
        else:
            cur += ch
    return cur
```

运行：`"3[a]2[bc]"` → `"aaabcbc"`，`"3[a2[c]]"` → `"accaccacc"`，`"2[abc]3[cd]ef"` → `"abcabccdcdcdef"`，`"abc3[cd]xyz"` → `"abccdcdcdxyz"`，`"10[a]"` → `"aaaaaaaaaa"`，`"1[a]"` → `"a"`；嵌套 5000 层的 `"1[" * 5000 + "a" + "]" * 5000` → `"a"`，没有递归所以不会栈溢出。

**复杂度。** 时间 `O(L)`，`L` 是最终输出长度（字符串乘法和拼接的复制量与输出同阶）；空间 `O(d + L)`，`d` 是嵌套深度。

**写法要点。** 栈里存元组 `(prefix, times)`，弹出时直接解包 `prev, times = stack.pop()`；`str * int` 是 C 层的重复拼接，比 Python 循环快；`cur, num = "", 0` 同时重置两个变量；`ch.isdigit()` 判断数字字符，题目只有 ASCII 数字，安全。需要拼接超长字符串时，用 `list` 收集再 `"".join(...)` 比反复 `+=` 稳，在 CPython 里 `+=` 有原地优化，其他解释器没有。
