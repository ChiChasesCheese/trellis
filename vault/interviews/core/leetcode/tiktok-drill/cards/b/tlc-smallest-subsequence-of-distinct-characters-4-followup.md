---
id: tlc-smallest-subsequence-of-distinct-characters-4-followup
node: b.smallest-subsequence-of-distinct-characters
type: qa
step: 4
---
## Q
**LC 1081 不同字符的最小子序列**｜追问

面试官接着问：（1）能不能一遍扫描 `O(n)` 完成？（2）要字典序最大的结果？（3）每种字符要求至少保留 `k` 次呢？

## A
1. **单调栈，`O(n)`**：栈里保持当前最优前缀；扫到字母 `ch`，已在栈里就跳过；否则当栈顶比 `ch` 大并且栈顶字母后面还会出现，就弹出栈顶，再让 `ch` 入栈。

```python
def smallest_subsequence_stack(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}
    stack: list[str] = []
    in_stack: set[str] = set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
```

`"bcabc"` → `"abc"`，`"cbacdcbc"` → `"acdb"`，与窗口版一致。每个字符至多进出栈一次，空间 `O(Σ)`。
2. **字典序最大**：窗口版每轮挑窗口里最大的字母（并列仍取最靠左，用 `key=lambda j: (-ord(s[j]), j)` 或先取最大字符再 `index`）；栈版把弹栈比较改成 `stack[-1] < ch`。`"cbacdcbc"` → `"cbad"`。
3. **长度固定为 `k` 的最小子序列**（LC 1673 找出最具竞争力的子序列）：同样的单调栈，弹栈多了一个条件——弹掉栈顶之后，剩下的数还要够凑满 `k` 个。

```python
def most_competitive(nums: list[int], k: int) -> list[int]:
    stack: list[int] = []
    n = len(nums)
    for i, x in enumerate(nums):
        while stack and stack[-1] > x and len(stack) - 1 + (n - i) >= k:
            stack.pop()                            # 弹掉后剩下的数还够凑满 k 个才可以弹
        if len(stack) < k:
            stack.append(x)
    return stack
```

`most_competitive([3,5,2,6], 2)` → `[2, 6]`，`most_competitive([2,4,3,3,5,4,9,6], 4)` → `[2, 3, 3, 4]`。

**Python 提醒**：`min(..., key=s.__getitem__)` 里的 `key` 只返回字符，并列时保留迭代中先遇到的元素；如果需要"并列取最靠右"，要把下标放进键里，写成 `key=lambda j: (s[j], -j)`。
