---
id: tlc-remove-duplicate-letters-4-followup
node: a.remove-duplicate-letters
type: qa
step: 4
---
## Q
**LC 316 去除重复字母**｜追问

面试官接着问：（1）要字典序**最大**的结果？（2）这个单调栈和「移掉 K 位数字」（LC 402）有什么关系？（3）字母表很大（不止 26）时还线性吗？

## A
1. **字典序最大**：把弹栈条件里的比较翻转，`stack[-1] < ch`，其余不变。`"cbacdcbc"` → `"cbad"`，`"bcabc"` → `"cab"`。

```python
def largest_distinct(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}
    stack: list[str] = []
    seen: set[str] = set()
    for i, ch in enumerate(s):
        if ch in seen:
            continue
        while stack and stack[-1] < ch and last[stack[-1]] > i:
            seen.discard(stack.pop())
        stack.append(ch)
        seen.add(ch)
    return "".join(stack)
```
2. **LC 402**：同样是"遇到更小的数字就弹掉前面更大的"，但少了"后面还会出现"这个条件，换成"最多还能删 `k` 个"的预算；最后预算没用完就从末尾截掉，并去掉前导零。

```python
def remove_k_digits(num: str, k: int) -> str:
    stack: list[str] = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    return "".join(stack[:len(stack) - k]).lstrip("0") or "0"
```

`remove_k_digits("1432219", 3)` → `"1219"`，`remove_k_digits("10200", 1)` → `"200"`，`remove_k_digits("10", 2)` → `"0"`。
3. **字母表很大**：单调栈本身仍然是 `O(n)`，每个字符至多进出一次，`last` 字典和 `in_stack` 集合的操作都是 `O(1)`，字母表大小只影响空间 `O(Σ)`，不影响时间。另一种"每步选最小的可行字母再检查后缀"的写法是 `O(Σ * n)`，字母表大时反而慢（见 LC 1081）。

**Python 提醒**：`"".join(stack[:len(stack) - k])` 里 `k` 为 `0` 时要写成 `len(stack) - k` 而不是 `stack[:-k]`，后者在 `k == 0` 时得到空列表。
