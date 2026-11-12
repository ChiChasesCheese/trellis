---
slug: greatest-common-divisor-of-strings
---
## Q
**LC 1071 字符串的最大公因子**｜Easy

`t` 能除尽 `s` 当且仅当 `s` 是 `t` 重复若干次。求最长的字符串 `x`，同时除尽 `str1` 和 `str2`，不存在返回 `""`。

## A
**一句话。** `str1 + str2 == str2 + str1` 说明两串由同一个串重复而成，答案是前 `gcd(长度1, 长度2)` 个字符。

```python
def gcd_of_strings(str1, str2):
    if str1 + str2 != str2 + str1:
        return ""
    return str1[:gcd(len(str1), len(str2))]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 不做拼接检查直接取 `gcd` 前缀：`("LEET", "CODE")` 得 `"LEET"`，应为 `""`。
- 拼接相等就返回较短串：`("ABABAB", "ABAB")` 得 `"ABAB"`，它除不尽 `"ABABAB"`，应为 `"AB"`。

**追问。**
- 多个字符串的最大公因子？：`reduce` 两两合并，任一步得 `""` 就一直是 `""`。
- 不想靠拼接技巧呢？：枚举 `gcd` 的约数长度，用前缀重复校验。

**同模式。** LC 459 重复的子字符串、LC 686 重复叠加字符串匹配、LC 28 找出字符串中第一个匹配项的下标
