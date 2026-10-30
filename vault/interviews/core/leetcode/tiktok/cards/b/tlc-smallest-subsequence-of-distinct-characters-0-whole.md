---
id: tlc-smallest-subsequence-of-distinct-characters-0-whole
node: b.smallest-subsequence-of-distinct-characters
type: qa
---
## Q
**LC 1081 不同字符的最小子序列**｜Medium · LC 字节 热度 88/100

返回字符串 `s` 的字典序最小的子序列，要求该子序列包含 `s` 中出现过的每一种字符，且每种恰好一次。`1 <= s.length <= 1000`，`s` 由小写英文字母组成。例：`"bcabc"` → `"abc"`；`"cbacdcbc"` → `"acdb"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 逐位贪心：每一位在一个"安全窗口"里挑最小的、还没用过的字母——窗口从当前位置到 `deadline`，`deadline` 是所有还没放的字母里最晚出现位置的最小值（再往后选就会让某个字母永远出现不了）；选中后从它的下一位继续。至多 26 轮，`O(26n)`。

**识别。** 「子序列 + 字典序最小 + 每种字符恰好一次」；字典序比较先看前面的字符，所以应该**从前往后一位一位地**选最小的可行字母。`n <= 1000`、字母只有 26 种，每一位花 `O(n)` 也远远够用。

**推导。** 暴力：枚举所有恰好包含每种字母一次的子序列取最小，指数级。洞察一：第一位尽量小，但不能小到后面凑不齐；一个字母 `c` 可以放在位置 `i`，当且仅当其余还没放的字母在 `i` 之后（含 `i`）都还能找到，即 `i <= min(各字母最后出现的位置)`，这就是 `deadline`。洞察二：同一个字母，选最靠左的出现位置，给后面留下最多的选择。所以每一轮在 `s[pos : deadline + 1]` 里挑最小的未用字母（并列取最靠左），然后 `pos` 移到它后面。

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

运行：`"bcabc"` → `"abc"`；`"cbacdcbc"` → `"acdb"`；`"a"` → `"a"`；`"aaaa"` → `"a"`；`"abacb"` → `"abc"`；`"ecbacba"` → `"eacb"`；`1000` 个随机小写字母 → 长度 `26`。

**复杂度。** 时间 `O(Σ * n)`，`Σ = 26`：至多 26 轮，每轮扫描不超过 `n` 个位置；空间 `O(Σ)`。

**易错点。**
- 不能忽略 `deadline`，直接挑全局最小字母：`"bcab"` 会先选 `a`（位置 2），之后 `c` 再也找不到，结果成了缺字母的 `"ab"`，正确是 `"bca"`。
- 并列时必须取最靠左的出现位置：`min` 对相同的键保留第一个，`range` 递增，正好满足。
- 窗口里要排除已经用过的字母（`s[j] in remaining`），否则会重复选。

**追问。**
- 更快的写法：316 里的单调栈，一遍扫描 `O(n)`——遇到更小的字母就弹掉后面还会出现的较大栈顶。
- 要字典序最大：每轮挑窗口里最大的字母，并列仍取最靠左。
- 字母表很大时：`remaining` 和 `last` 的规模随之变大，每轮求 `deadline` 变成 `O(Σ)`，此时单调栈更合适。

**同模式。** LC 316 去除重复字母（同一题）、LC 402 移掉 K 位数字、LC 321 拼接最大数、LC 738 单调递增的数字。
