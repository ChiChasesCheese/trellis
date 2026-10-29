---
id: tlc-remove-k-digits-4-followup
node: a.remove-k-digits
type: qa
step: 4
---
## Q
**LC 402 移掉 K 位数字**｜追问

面试官接着问：（1）改成保留 `m` 位使数字**最大**？（2）要求去除重复字母使字典序最小（LC 316）？（3）数字有 `10^6` 位，Python 有什么要注意的？

## A
1. **保留 `m` 位取最大。** 弹栈条件反过来，额度是 `len(num) - m`，最后截取前 `m` 位：

```python
def max_subsequence(num: str, m: int) -> str:
    drop = len(num) - m                          # 一共可以丢掉多少位
    stack: list[str] = []
    for d in num:
        while drop and stack and stack[-1] < d:  # 栈顶比新数字小：丢掉栈顶更优
            stack.pop()
            drop -= 1
        stack.append(d)
    return "".join(stack[:m])
```

`("1432219", 4)` → `"4329"`。
2. **LC 316 去除重复字母。** 仍是单调栈，弹栈前再加两个条件：栈顶字母在后面还会出现；新字母不在栈里（已在栈里就直接跳过）。额度由"后面是否还有"决定，不再是固定的 `k`。
3. **超长字符串。** 全程保持字符串和列表，不要 `int(num)`；`"".join(stack)` 是线性的，不要在循环里反复拼接字符串。

**Python 提醒**：`list[: len(stack) - k]` 与 `list[:-k]` 在 `k == 0` 时截然不同：前者是整个列表，后者是空列表；需要"去掉末尾 `k` 个"时，永远用前者，或 `del stack[len(stack) - k:]`。
