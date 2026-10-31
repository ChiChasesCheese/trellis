---
id: tlc-greatest-common-divisor-of-strings-0-whole
node: b.greatest-common-divisor-of-strings
type: qa
---
## Q
**LC 1071 字符串的最大公因子**｜Easy · LC TikTok 全时段热度 50/100

对于字符串 `s` 和 `t`，只有 `s = t + t + … + t`（`t` 自身连接一次或多次）时，才说 `t` 能除尽 `s`。给定 `str1` 和 `str2`，返回最长的字符串 `x`，使得 `x` 能同时除尽 `str1` 和 `str2`；不存在就返回 `""`。`1 <= str1.length, str2.length <= 1000`，字符串由大写英文字母组成。例：`("ABCABC", "ABC")` → `"ABC"`；`("ABABAB", "ABAB")` → `"AB"`；`("LEET", "CODE")` → `""`；`("AAAAAB", "AAA")` → `""`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先判断公因子串是否存在：`str1 + str2 == str2 + str1` 当且仅当两个字符串都是同一个串的若干次重复；存在时，答案就是 `str1` 的前 `gcd(len(str1), len(str2))` 个字符。`O(n)`。

**识别。** 「`t` 能除尽 `s`」是整除在字符串上的版本，「最大公因子」提示长度取 `gcd`（最大公约数），内容由前缀决定。长度只到 `1000`，枚举也能过，但拼接比较加 `gcd` 是 `O(n)` 的优雅解法，面试里值得写出来。

**推导。** 暴力：长度 `L` 从 `min(len1, len2)` 往下枚举，只看同时整除两个长度的 `L`，取 `str1[:L]`，检查它重复若干次是否等于 `str1` 和 `str2`，`O(n · 约数个数)`。洞察一：若公因子串 `x` 存在，`str1 = x^a`，`str2 = x^b`，所以 `str1 + str2 = x^(a+b) = str2 + str1`，两种拼接顺序相同。洞察二（反方向）：若两种拼接顺序相同，则二者是同一个原串的幂，最长的公因子串长度恰好是 `gcd(len1, len2)`。两个洞察合起来，答案就是一次比较加一次切片。

```python
from math import gcd


def gcd_of_strings(str1: str, str2: str) -> str:
    if str1 + str2 != str2 + str1:         # 有公因子串 <=> 两种拼接顺序结果一致
        return ""
    return str1[:gcd(len(str1), len(str2))]
```

运行：`("ABCABC", "ABC")` → `'ABC'`，`("ABABAB", "ABAB")` → `'AB'`，`("LEET", "CODE")` → `''`，`("AAAAAB", "AAA")` → `''`，`("A", "A")` → `'A'`，`("AB", "BA")` → `''`，`("A" * 1000, "A" * 999)` → `'A'`。

**复杂度。** 时间 `O(n)`：拼接与比较各 `O(n)`，`gcd` 是 `O(log n)`；空间 `O(n)`（两个拼接字符串）。

**易错点。**
- 只取 `gcd` 长度的前缀，不做拼接检查：`("LEET", "CODE")` 得到 `"LEET"`，`("AAAAAB", "AAA")` 得到 `"AAA"`，正确都是 `""`。
- 拼接相等就返回较短的字符串：`("ABABAB", "ABAB")` 得到 `"ABAB"`，它并不能除尽 `"ABABAB"`，正确是 `"AB"`。
- 把长度的最大公约数当成答案本身返回：返回的是字符串，要切片。

**追问。**
- 多个字符串的最大公因子：`functools.reduce(gcd_of_strings, strs)`，两两合并，任何一步得到 `""` 就一直是 `""`。
- 最短的公共倍串（两个都能整除它的最短串）：拼接相等时取 `str1 * (len(str2) // gcd(len1, len2))`，长度是 `lcm`。
- 不想靠拼接技巧：枚举 `gcd` 的约数长度，用前缀重复校验，`O(n · d(g))`。

**同模式。** LC 459 重复的子字符串、LC 686 重复叠加字符串匹配、LC 1668 最大重复子字符串、LC 28 找出字符串中第一个匹配项的下标。
