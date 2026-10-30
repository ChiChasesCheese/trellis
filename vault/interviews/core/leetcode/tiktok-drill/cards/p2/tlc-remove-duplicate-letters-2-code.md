---
id: tlc-remove-duplicate-letters-2-code
node: p2.remove-duplicate-letters
type: qa
step: 2
---
## Q
**LC 316 去除重复字母**｜写出 Python 实现

`s` 由小写英文字母组成，`1 <= s.length <= 10^4`。去掉重复字母使每种字母恰好出现一次，结果必须是 `s` 的子序列，并且字典序最小。

## A
**思路。** 先记录每个字母最后一次出现的下标。从左到右扫描，字母已经在栈里就跳过；否则当栈顶比当前字母大、并且栈顶字母后面还会出现时，弹出栈顶，最后把当前字母入栈。

```python
def remove_duplicate_letters(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}       # 每个字母最后一次出现的下标
    stack: list[str] = []
    in_stack: set[str] = set()
    for i, ch in enumerate(s):
        if ch in in_stack:                         # 已经放好了，跳过（先放的位置一定不差）
            continue
        # 栈顶比 ch 大，且栈顶后面还会再出现：弹掉它，换更小的字母占前面的位置
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
```

运行：`"bcabc"` → `"abc"`；`"cbacdcbc"` → `"acdb"`；`"a"` → `"a"`；`"aaaa"` → `"a"`；`"abacb"` → `"abc"`；`"ecbacba"` → `"eacb"`；`10^4` 个随机小写字母 → 长度 `26`。

**复杂度。** 时间 `O(n)`：每个字符至多入栈一次、出栈一次；空间 `O(Σ)`，`Σ = 26`。

**写法要点。** 字典推导 `{ch: i for i, ch in enumerate(s)}` 后出现的下标覆盖先出现的，一行得到"最后出现位置"；`in_stack` 集合让"是否已在栈里"从 `O(26)` 降到 `O(1)`；`set.discard` 在元素不存在时不报错（`remove` 会抛 `KeyError`）；字符串之间直接用 `>` 比较字典序，单个字母比较等价于比较码点。
