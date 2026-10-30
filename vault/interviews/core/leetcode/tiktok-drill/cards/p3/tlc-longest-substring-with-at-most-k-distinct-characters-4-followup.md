---
id: tlc-longest-substring-with-at-most-k-distinct-characters-4-followup
node: p3.longest-substring-with-at-most-k-distinct-characters
type: qa
step: 4
---
## Q
**LC 340 至多包含 K 个不同字符的最长子串**｜追问

面试官接着问：（1）字符是流式到来的，`s` 无法整个读入内存？（2）能不能不用计数、只记每个字符最近出现的位置？（3）窗口只增不缩的写法是什么？

## A
1. **流式。** 只需窗口内的计数，空间 `O(k)`，与 `s` 的长度无关；窗口左端的字符要能取到，所以要保留窗口内的字符（至多“最长合法子串”那么长）。如果要的只是长度，可以用下面第 2 种，只保留每种字符最近一次出现的位置，空间严格 `O(k)`。
2. **最近出现位置。** 用 `OrderedDict` 存「字符 → 最近出现的下标」，每次访问把字符移到末尾；超过 `k` 种时，弹出最老的那个，`left` 设为它的下标加一：
```python
from collections import OrderedDict

def k_distinct_last_seen(s: str, k: int) -> int:
    last: OrderedDict[str, int] = OrderedDict()
    left = best = 0
    for right, ch in enumerate(s):
        last.pop(ch, None)                  # 先删再放，等于把 ch 移到末尾
        last[ch] = right
        if len(last) > k:
            _, pos = last.popitem(last=False)   # 弹出最久没出现的字符
            left = pos + 1                  # 窗口左端越过它最后一次出现的位置
        best = max(best, right - left + 1)
    return best
```
`("eceba", 2)` → `3`，`("aa", 1)` → `2`，`("abc", 0)` → `0`。每步 `O(1)`，空间 `O(k)`。
3. **只增不缩。** 种类数超了只缩一步（`if`），窗口以固定宽度平移；窗口的宽度从不变小，最终 `len(s) - left` 就是答案。更短，但“为什么不会错”的论证更绕，面试里先写 `while` 版。

**Python 提醒**：`Counter` 的 `del count[key]` 与 `count[key] = 0` 不同，后者保留键；另外 `Counter.subtract` 和减法运算 `-` 都可能产生零或负计数，只有减法运算符 `c1 - c2` 会丢弃非正计数。
