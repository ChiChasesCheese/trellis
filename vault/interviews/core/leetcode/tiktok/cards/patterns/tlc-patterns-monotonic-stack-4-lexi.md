---
id: tlc-patterns-monotonic-stack-4-lexi
node: patterns.monotonic-stack
type: qa
step: 4
---
## Q
**单调栈（Monotonic Stack）｜字典序最小：去重字母（LC 316、1081）与移掉 K 位数字（LC 402）**

为什么「保持栈递增，遇到更小的就弹出栈顶」能得到字典序最小的结果？弹出时要满足什么条件才不丢字符？

## A
想让结果的字典序小，就要让**靠前的位置尽量小**。新字符 `ch` 比栈顶小，把栈顶换成 `ch` 能让这个位置变小，前提是被弹出的字符之后**还能再次出现**（或者还有删除额度）。

```python
def remove_duplicate_letters(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}   # 每个字符最后出现的位置
    st: list[str] = []
    in_st: set[str] = set()
    for i, ch in enumerate(s):
        if ch in in_st:
            continue                           # 已在结果里，保持它更靠前的位置
        while st and st[-1] > ch and last[st[-1]] > i:   # 栈顶更大且后面还会再出现
            in_st.discard(st.pop())
        st.append(ch)
        in_st.add(ch)
    return "".join(st)

def remove_k_digits(num: str, k: int) -> str:
    st: list[str] = []
    for ch in num:
        while k and st and st[-1] > ch:        # 前面的数字更大：删掉它
            st.pop()
            k -= 1
        st.append(ch)
    if k:
        st = st[:-k]                           # 栈已递增，剩余额度删末尾
    return "".join(st).lstrip("0") or "0"
```

运行：`remove_duplicate_letters("bcabc")` → `"abc"`，`("cbacdcbc")` → `"acdb"`；`remove_k_digits("1432219", 3)` → `"1219"`，`("10200", 1)` → `"200"`，`("10", 2)` → `"0"`。

- 漏掉 `last[st[-1]] > i` 的反例：`"cba"` 本身无重复，正确是 `"cba"`；漏掉判断会一路弹出，只剩 `"a"`。
- LC 402 要处理前导零（`lstrip("0")`）和空结果（`or "0"`）。
- 时间 `O(n)`，空间 `O(n)`（LC 316 的字符集只有 26，栈至多 26）。
