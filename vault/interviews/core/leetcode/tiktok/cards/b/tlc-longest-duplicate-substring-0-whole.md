---
id: tlc-longest-duplicate-substring-0-whole
node: b.longest-duplicate-substring
type: qa
---
## Q
**LC 1044 最长重复子串**｜Hard · CodeTop 国内累计 8 次 · 最近 2026-09-02（国内 CodeTop）

给一个字符串 `s`，考虑它所有的**重复子串**：即 `s` 的（连续）子串，在 `s` 中出现 `2` 次或更多次，这些出现之间**可能重叠**。返回任意一个长度最长的重复子串；`s` 不含重复子串时返回 `""`。`2 <= s.length <= 3 * 10^4`，`s` 由小写英文字母组成。例：`s = "banana"` → `"ana"`（在下标 `1` 和 `3` 处出现，两次出现重叠）；`s = "abcd"` → `""`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二分答案长度 `L`（存在长度 `L` 的重复子串 ⇒ 存在长度 `L - 1` 的，所以可以二分）；每个 `L` 用滚动哈希（Rabin-Karp）在 `O(n)` 内判断是否有两个相同的长度 `L` 窗口，哈希相同再逐字比对；总时间 `O(n log n)`。

**识别。** 「最长 + 重复子串 + `n = 3 * 10^4`」：枚举所有子串放进集合是 `O(n^2)` 个子串、每个还要 `O(n)` 的切片和哈希，远超限制。答案有**单调性**（把重复子串去掉一个字符仍重复）→ 二分答案；判定问题「长度 `L` 的窗口有没有重复」靠滚动哈希做到 `O(n)`。近似但不同：LC 1062 的 `n <= 2000`，集合加切片就够；LC 718 最长重复子数组是两个数组之间的公共子串。

**推导。** 暴力：对每个长度，把所有窗口切片放进集合，总 `O(n^2 · n)`。第一步浪费：长度逐个试。单调性让它变成二分，只需要 `log n` 次判定。第二步浪费：判定时每个窗口都重新切片 / 计算哈希要 `O(L)`。滚动哈希把窗口右移一格的更新降到 `O(1)`：`h = h * base - 出去的字符 * base^L + 进来的字符`（对大质数取模）。哈希可能碰撞，所以哈希相同还要比较实际子串；随机底数和 `2^61 - 1` 这样的大模数让碰撞概率可以忽略，验证的开销期望是常数。

```python
import random


def longest_dup_substring(s: str) -> str:
    n = len(s)
    nums = [ord(c) - 96 for c in s]        # 'a'..'z' -> 1..26
    mod = (1 << 61) - 1
    base = random.randrange(1 << 20, mod)  # 随机底数：防止被构造数据卡哈希

    def find(length: int) -> int:          # 返回某个长度为 length 的重复子串的起点，没有则 -1
        top = pow(base, length, mod)       # base^length，用来滚掉最左边的字符
        h = 0
        for x in nums[:length]:
            h = (h * base + x) % mod
        seen = {h: [0]}                    # 哈希 -> 起点列表（链式，应对碰撞）
        for i in range(1, n - length + 1):
            h = (h * base - nums[i - 1] * top + nums[i + length - 1]) % mod
            for j in seen.get(h, ()):
                if s[j:j + length] == s[i:i + length]:     # 哈希相同再逐字比对，杜绝假阳性
                    return i
            seen.setdefault(h, []).append(i)
        return -1

    lo, hi, start = 1, n - 1, -1           # 答案长度在 [0, n-1]；"有长度 L 的重复" 对 L 单调
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if (idx := find(mid)) != -1:
            start, best, lo = idx, mid, mid + 1
        else:
            hi = mid - 1
    return s[start:start + best] if best else ""
```

运行：`"banana"` → `'ana'`，`"abcd"` → `''`，`"aa"` → `'a'`，`"aaa"` → `'aa'`；长度 `30000` 的全 `a` 串 → 长度 `29999`。

**复杂度。** 时间 `O(n log n)`（期望）：二分 `log n` 轮，每轮一次 `O(n)` 的滚动扫描，验证期望常数次比较；空间 `O(n)`。

**易错点。**
- 出现可以**重叠**：`"banana"` 里 `"ana"` 出现在下标 `1` 和 `3`，共用一个 `a`。若误以为必须不重叠，答案会退到长度 `2`（如 `"an"`），少了 `1`。
- 二分范围是 `[1, n - 1]`：长度 `n` 的子串只有一个，不可能重复；`find` 返回起点而不是布尔值，才能在二分结束时取出子串。
- 哈希相同不等于字符串相同：不比对就返回会有假阳性。滚动更新里 `nums[i - 1] * top` 做减法后取模，Python 的 `%` 总是非负，其他语言要补 `+ mod`。

**追问。**
- 不想用哈希：后缀数组 + 最长公共前缀（LCP），答案是相邻后缀 LCP 的最大值，`O(n log^2 n)`（或后缀自动机 `O(n)`）。
- 要求两次出现**不重叠**：`find` 里为每个哈希只记最早的起点，判定条件加上 `i - j >= length`。
- 出现至少 `k` 次：`seen` 里记录个数，达到 `k` 才返回。

**同模式。** LC 1062 最长重复子串、LC 718 最长重复子数组、LC 187 重复的DNA序列、LC 28 找出字符串中第一个匹配项的下标、LC 214 最短回文串。
