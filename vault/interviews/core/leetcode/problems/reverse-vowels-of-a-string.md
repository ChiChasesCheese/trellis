---
slug: reverse-vowels-of-a-string
---
## Q
**LC 345 反转字符串中的元音字母**｜Easy

给你字符串 `s`，仅反转字符串中的所有元音字母，并返回结果字符串。元音字母包括 `'a'`、`'e'`、`'i'`、`'o'`、`'u'`，大小写都算，可能出现多次。`1 <= s.length <= 3 * 10^5`，`s` 由可打印 ASCII 字符组成。例：`"IceCreAm"` → `"AceCreIm"`（元音依次是 `I e e A`，反转后写回）；`"leetcode"` → `"leotcede"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 对撞双指针 + 条件跳过：只在「满足条件的位置」之间做对称交换。

**一句话。** 左指针找下一个元音，右指针找上一个元音，两个都找到就交换并内移。

**识别。** 「只反转某一类字符、其余位置不动」= 两端指针各自跳过无关字符，同 LC 125；`n` 到 `3 * 10^5`，要 `O(n)`。

**推导。** 直觉做法：收集所有元音，反转，再按顺序写回，需要两趟和一份额外列表。对撞指针一趟完成：第 `i` 个元音一定与倒数第 `i` 个元音交换，指针相遇就结束。

```python
def reverse_vowels(s: str) -> str:
    vowels = set("aeiouAEIOU")  # 大小写都算元音
    chars = list(s)  # str 不可变，转成列表后原地交换
    left, right = 0, len(chars) - 1
    while left < right:
        if chars[left] not in vowels:  # 左边不是元音：左指针右移，不动右边
            left += 1
        elif chars[right] not in vowels:  # 右边不是元音：右指针左移
            right -= 1
        else:  # 两端都是元音：交换，再一起内移
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1
    return "".join(chars)
```

运行：`"IceCreAm"` → `"AceCreIm"`；`"leetcode"` → `"leotcede"`；`"bcd"`（无元音）→ `"bcd"`；`"a"` → `"a"`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（`str` 不可变，列表副本不可避免）；双指针本身 `O(1)`。

**易错点。**
- 漏掉大写元音：只用 `"aeiou"` 时 `"IceCreAm"` 得到 `"IceCreAm"`（两个 `e` 互换等于没动），正确答案是 `"AceCreIm"`。
- 交换后忘记同时移动两个指针，会在同一对元音上死循环。
- 用 `s[left], s[right] = ...` 直接改字符串会报 `TypeError`。

**同模式。** LC 125 验证回文串、LC 344 反转字符串、LC 11 盛最多水的容器、LC 283 移动零。
