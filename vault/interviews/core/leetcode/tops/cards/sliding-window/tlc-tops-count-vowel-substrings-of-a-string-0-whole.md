---
id: tlc-tops-count-vowel-substrings-of-a-string-0-whole
node: sliding-window.count-vowel-substrings-of-a-string
type: qa
---
## Q
**LC 2062 统计字符串中的元音子字符串（Count Vowel Substrings of a String）**｜Easy · 全公司热度第 176 名

子字符串是字符串中的一个连续（非空）的字符序列。元音子字符串是**仅**由元音（`'a'`、`'e'`、`'i'`、`'o'`、`'u'`）组成的子字符串，且必须包含**全部五种**元音。给你字符串 `word`，统计并返回 `word` 中元音子字符串的数目。`1 <= word.length <= 100`，`word` 仅由小写英文字母组成。例：`"aeiouu"` → `2`（`"aeiou"`、`"aeiouu"`）；`"unicornarihan"` → `0`；`"cuaieuouac"` → `7`；`"bbaeixoubb"` → `0`（含全部五种元音的子串都含辅音）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 按辅音切段 + 记录每种元音最后出现位置（last occurrence）数合法左端点。

**一句话。** 辅音把字符串切成若干纯元音段，每段内独立计算：对每个右端点 `i`，合法的左端点是 `[段起点, min(五个元音最后出现位置)]`，个数相加。

**识别。** 「子串必须恰好由某类字符组成，并且要覆盖全部 5 种」：先按不合格字符（辅音）分段，段内是「包含全部种类的子串数」。`n <= 100` 暴力 `O(n^2)` 也能过，但 `O(n)` 的写法能推广到大数据。

**推导。** 枚举起点向右延伸，用集合记元音种类，一旦集合大小为 5 就计一个，遇到辅音停止：`O(n^2)`（见拓展）。观察：固定右端点 `i`，子串 `[l, i]` 含全部 5 种元音，等价于 `l` 不超过每种元音的最后出现位置，即 `l <= min(last)`；同时 `l` 不能越过段起点。所以以 `i` 结尾的合法子串个数是 `min(last) - start + 1`。

```python
def count_vowel_substrings(word: str) -> int:
    ans = start = 0                              # start：当前连续元音段的起点
    last = dict.fromkeys("aeiou", -1)            # 每个元音在当前段内最后一次出现的下标
    for i, ch in enumerate(word):
        if ch not in last:                       # 辅音：段到此为止，全部重置
            start = i + 1
            last = dict.fromkeys("aeiou", -1)
            continue
        last[ch] = i
        lo = min(last.values())                  # 子串 [l, i] 含全部 5 个元音 <=> l 不超过每个元音的最后位置
        if lo >= start:                          # 五个元音在段内都出现过
            ans += lo - start + 1                # 合法的左端是 start..lo
    return ans
```

运行：`"aeiouu"` → `2`，`"unicornarihan"` → `0`，`"cuaieuouac"` → `7`，`"bbaeixoubb"` → `0`，`"a"` → `0`，`"aeiou"` → `1`。

**复杂度。** 时间 `O(n)`（每步对固定 5 个值取最小），空间 `O(1)`。

**拓展优化。**
- `n <= 100` 时更直白的写法：枚举起点，向右延伸并用集合记种类，遇到辅音停止，`O(n^2)`。

```python
def count_vowel_substrings_brute(word: str) -> int:    # n <= 100：枚举每个起点向右延伸，O(n^2)
    ans = 0
    for i in range(len(word)):
        seen: set[str] = set()
        for ch in word[i:]:
            if ch not in "aeiou":
                break
            seen.add(ch)
            ans += len(seen) == 5
    return ans
```

**易错点。**
- 遇到辅音不重置 `last` 和 `start`：`"bbaeixoubb"` 会把含 `x` 的 `"aeixou"` 数进去，输出 `3`，正确 `0`。
- 忘记检查 `lo >= start`：某个元音还没出现时 `lo = -1`，`"baei"` 会累加负数，输出 `-3`，正确 `0`。
- 每个纯元音段只数一次：`"aeiouu"` 得到 `1`，正确 `2`（`"aeiou"` 和 `"aeiouu"` 都算）。

**同模式。** LC 2063 所有子字符串中的元音、LC 992 K 个不同整数的子数组、LC 1456 定长子串中元音的最大数目、LC 3 无重复字符的最长子串。
