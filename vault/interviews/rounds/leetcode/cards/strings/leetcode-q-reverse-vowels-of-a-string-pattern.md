---
id: leetcode-q-reverse-vowels-of-a-string-pattern
node: strings.string
type: qa
anki: 1787268625387
tags: [lc::345, leetcode, pattern, recall]
---
## Q
如何用双指针原地反转字符串中的元音字母（LeetCode 345）？

## A
用左右双指针从两端向中间扫描：左指针跳过非元音字符，右指针跳过非元音字符，当两者都停在元音上时交换，然后各自向中间移动一步，直到 left >= right。判断元音时用小写映射到集合（{a,e,i,o,u}）来同时兼容大小写。相比额外收集元音下标再逐个 pop 出栈的写法，双指针版本更省心且是该模式的标准解法。

**Evidence**

```
def reverseVowels0(self, s: str) -> str:
    lowers = 'aeiou'
    uppers = lowers.upper()
    vowels = set(lowers + uppers)
    left, right = 0, len(s) - 1
    s = list(s)
    while left < right:
        while left < right and s[left] not in vowels:
            left += 1
        while left < right and s[right] not in vowels:
            right -= 1
        if left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
    return "".join(s)
```

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F345%20-%20Reverse%20Vowels%20of%20a%20String)
