---
slug: valid-palindrome
---
## Q
**LC 125 验证回文串**｜Easy

忽略大小写，只看字母和数字，判断字符串 `s` 是否正着读反着读一样（空串算回文）。

## A
**一句话。** 双指针从两端向中间走，各自跳过非字母数字，忽略大小写比较。

```python
def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 内层 `while` 漏了 `i < j`：`" "` 或 `".,"` 全是符号时指针越界。
- 用 `isalpha` 代替 `isalnum`：`"0P"` 会跳掉 `0`，错判成 `True`。
- 忘了统一大小写：`"Aa"` 应为 `True`。

**追问。**
- 允许删除一个字符（LC 680）？：不等时分别试删左、删右，再判断剩余部分。
- 不想用 `isalnum`？：先预处理成只含小写字母数字的串再比较，空间 `O(n)`。

**同模式。** LC 680 验证回文串 II、LC 5 最长回文子串、LC 345 反转字符串中的元音字母、LC 11 盛最多水的容器
