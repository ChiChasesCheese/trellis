---
slug: reverse-vowels-of-a-string
---
## Q
**LC 345 反转字符串中的元音字母**｜Easy

只反转字符串 `s` 中的元音（`aeiou`，大小写都算），其余字符位置不变。

## A
**一句话。** 双指针从两端向内找元音，两端都是元音就交换。

```python
def reverse_vowels(s):
    vowels = set("aeiouAEIOU")
    chars = list(s)              # str 不可变
    l, r = 0, len(chars) - 1
    while l < r:
        if chars[l] not in vowels:
            l += 1
        elif chars[r] not in vowels:
            r -= 1
        else:
            chars[l], chars[r] = chars[r], chars[l]
            l += 1
            r -= 1
    return "".join(chars)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 漏掉大写元音：`"IceCreAm"` 应得 `"AceCreIm"`。
- 交换后不同时移动两个指针：在同一对元音上死循环。

**追问。**
- 不想建列表？：先收集元音按逆序，再遍历 `s` 遇到元音就弹一个，也是 `O(n)`。
- 只反转字母（LC 917）？：判断条件换成 `isalpha`。

**同模式。** LC 125 验证回文串、LC 344 反转字符串、LC 11 盛最多水的容器、LC 283 移动零
