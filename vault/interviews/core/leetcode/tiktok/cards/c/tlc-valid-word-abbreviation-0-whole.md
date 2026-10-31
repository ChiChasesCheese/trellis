---
id: tlc-valid-word-abbreviation-0-whole
node: c.valid-word-abbreviation
type: qa
---
## Q
**LC 408 有效单词缩写**｜Easy · LC TikTok 全时段热度 25/100

字符串可以用**缩写**表示：把任意数量的**不相邻**的子字符串替换为它们的长度。例如 `"substitution"` 可以缩写为 `"s10n"`、`"sub4u4"`、`"12"`、`"su3i1u2on"`、`"substitution"`（不替换）。不合法的缩写：`"s55n"`（两处缩写相邻）、`"s010n"`（有前导零）、`"s0ubstitution"`（缩写是一个空字符串）。给你字符串 `word` 和缩写 `abbr`，判断 `abbr` 是否可以是 `word` 的缩写。`1 <= word.length <= 20`，`word` 仅由小写英文字母组成，`1 <= abbr.length <= 10`，`abbr` 由小写英文字母和数字组成，`abbr` 中的所有数字均符合 32 位整数范围。例：`word = "internationalization", abbr = "i12iz4n"` → `true`；`word = "apple", abbr = "a2e"` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 双指针同时扫 `word` 和 `abbr`：遇到字母就要求两边相等并同时前进；遇到数字就读出整个数（不能以 `0` 开头），让 `word` 的指针跳过这么多位，最后两个指针都恰好走到末尾，`O(len(word) + len(abbr))`。

**识别。** 「一个串是另一个串的压缩/模式形式」：两个串各用一个指针，一个字符一个字符地对齐，数字让 `word` 的指针跳跃，是双指针匹配的标准形式。

**推导。** 字母必须逐位匹配；一段连续数字表示一次缩写，数值就是跳过的字符数。非法情形在读数字时一并处理：以 `0` 开头的数字（含单独的 `0`）都不合法。因为缩写互不相邻，连续数字一定属于同一次缩写，要整段读完再跳。结尾要求 `word` 和 `abbr` 都恰好用完；跳过的距离超过 `word` 剩余长度，指针越界，也属于不合法。

```python
def valid_word_abbreviation(word: str, abbr: str) -> bool:
    m, n = len(word), len(abbr)
    i = j = 0                                    # i 指向 word，j 指向 abbr
    while i < m and j < n:
        if abbr[j].isdigit():
            if abbr[j] == "0":
                return False                     # 前导零，或者缩写成长度 0 的空串
            k = j
            while k < n and abbr[k].isdigit():   # 整段数字读完，连续数字属于同一次缩写
                k += 1
            i += int(abbr[j:k])                  # word 跳过这么多个字符
            j = k
        else:
            if word[i] != abbr[j]:
                return False
            i += 1
            j += 1
    return i == m and j == n                     # 两边都恰好用完；跳过头 i > m 也会返回 False
```

运行：`("internationalization", "i12iz4n")` → `True`，`("apple", "a2e")` → `False`；`("a", "1")` → `True`，`("a", "a0")` → `False`，`("substitution", "s010n")` → `False`，`("substitution", "s55n")` → `False`，`("substitution", "12")` → `True`。

**复杂度。** 时间 `O(len(word) + len(abbr))`，空间 `O(1)`。

**拓展优化。**
- 正则表达式一行做完：把每段数字换成 `.{k}`，再 `fullmatch`。代价是前导零要单独检查，且依赖正则引擎，但适合快速验证。

```python
import re


def valid_word_abbreviation_regex(word: str, abbr: str) -> bool:
    if re.search(r"(?<!\d)0", abbr):             # 以 0 开头的数字段（含单独的 0）不合法
        return False
    pattern = re.sub(r"\d+", lambda m: f".{{{int(m.group())}}}", abbr)   # 数字 k -> 恰好 k 个任意字符
    return re.fullmatch(pattern, word) is not None
```

**易错点。**
- 没拒绝数字 `0`：`("ab", "a0b")` 得到 `True`（`i += 0` 后继续匹配 `b`），正确是 `False`。
- 一位一位地读数字：`("internationalization", "i12iz4n")` 把 `12` 当成 `1` 和 `2` 分别处理，返回 `False`，正确是 `True`。
- 结尾只检查 `i == m`：`abbr` 还有剩余字符时也该返回 `False`，例如 `("a", "ab")`。

**追问。**
- 缩写数字超过 32 位：Python 的 `int` 不溢出，但要提前判断 `i` 是否已经越界，避免无意义的大数运算。
- 反过来生成所有缩写（LC 320）：位掩码枚举哪些字符被缩写，连续被缩写的合成一个数字。

**同模式。** LC 320 列举单词的全部缩写、LC 411 最短独占单词缩写、LC 527 单词缩写、LC 392 判断子序列、LC 44 通配符匹配。
