---
id: tlc-smallest-subsequence-of-distinct-characters-2-code
node: b.smallest-subsequence-of-distinct-characters
type: qa
step: 2
---
## Q
**LC 1081 不同字符的最小子序列**｜写出 Python 实现

`s` 由小写英文字母组成，`1 <= s.length <= 1000`。返回 `s` 的字典序最小的子序列，要求它包含 `s` 中的每一种字符且每种只出现一次。用"逐位贪心加安全窗口"的写法。

## A
**思路。** 记录每个字母最后一次出现的位置。每一轮，`deadline` 取未放字母最后出现位置的最小值；在 `s[pos : deadline + 1]` 里挑还没用过的最小字母（并列取最靠左），放进结果，`pos` 移到它的下一位。直到所有字母都放完。

```python
def smallest_subsequence(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}       # 每个字母最后一次出现的下标
    remaining = set(s)                             # 还没放进结果的字母
    result: list[str] = []
    pos = 0                                        # 下一个字母只能从 s[pos:] 里选
    while remaining:
        deadline = min(last[c] for c in remaining)  # 选的位置不能超过它，否则某个字母再也出现不了
        # 在 s[pos : deadline + 1] 里挑还没用过的最小字母；min 遇到并列取最靠左的
        i = min((j for j in range(pos, deadline + 1) if s[j] in remaining), key=s.__getitem__)
        result.append(s[i])
        remaining.discard(s[i])
        pos = i + 1
    return "".join(result)
```

运行：`"bcabc"` → `"abc"`；`"cbacdcbc"` → `"acdb"`；`"a"` → `"a"`；`"aaaa"` → `"a"`；`"abacb"` → `"abc"`；`"ecbacba"` → `"eacb"`。

**复杂度。** 时间 `O(Σ * n)`，`Σ = 26`；空间 `O(Σ)`。

**写法要点。** `min(生成器, key=s.__getitem__)` 按字母比较，遇到并列保留第一个，对应最靠左的位置；`s.__getitem__` 是现成的"下标到字符"函数，比 `lambda j: s[j]` 简洁；生成器表达式不建临时列表；`set.discard` 在元素缺失时不报错；`min(last[c] for c in remaining)` 对非空集合调用，循环条件保证 `remaining` 非空。
