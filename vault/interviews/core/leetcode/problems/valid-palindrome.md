---
slug: valid-palindrome
---
## Q
**LC 125 验证回文串**｜Easy

把所有大写字母转成小写、并去掉所有非字母数字字符之后，如果短语正着读和反着读一样，它就是回文串。给定字符串 `s`，判断它是不是回文串。`1 <= s.length <= 2 * 10^5`，`s` 只含可打印 ASCII 字符。例：`"A man, a plan, a canal: Panama"` → `true`；`"race a car"` → `false`；`" "` → `true`（去掉非字母数字后是空串，空串是回文）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 对撞双指针（two pointers from both ends）：回文就是两端向中间逐对相等。

**一句话。** 左右指针各自跳过非字母数字字符，忽略大小写比较，不等就返回 `False`，相遇则为 `True`。

**识别。** 「正着读等于倒着读」= 首尾配对，对撞指针；`n` 到 `2 * 10^5`，要 `O(n)`。

**推导。** 直觉做法：先清洗成新字符串，再和反转比较，`O(n)` 时间但多一份 `O(n)` 空间。清洗只是为了跳过噪声字符，指针本身可以跳过它们，所以不需要新串。

**简单解法。** 先过滤再和反转比较：`t = [c.lower() for c in s if c.isalnum()]; return t == t[::-1]`，代码一行，面试里同样可以接受；上面的双指针只是把额外的 `O(n)` 空间省掉。

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():  # 两端各自跳过非字母数字字符
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():  # 忽略大小写比较
            return False
        left += 1
        right -= 1
    return True  # 指针相遇说明每一对都配上了；全是符号的串也走到这里，空串视为回文
```

运行：`"A man, a plan, a canal: Panama"` → `True`；`"race a car"` → `False`；`" "` → `True`；`".,"` → `True`。

**复杂度。** 时间 `O(n)`，每个下标最多被指针经过一次；空间 `O(1)`。

**易错点。**
- 内层 `while` 也要带 `left < right`：`" "` 或 `".,"` 全是符号时，缺了它指针会越界（`IndexError`）。
- 要用 `isalnum`，不是 `isalpha`：`"0P"` 正确答案是 `False`（`"0p"` 不对称），用 `isalpha` 会把 `0` 跳掉，只剩 `"p"`，错判成 `True`。
- 比较前统一大小写，`"Aa"` 应为 `True`。

**同模式。** LC 680 验证回文串 II、LC 5 最长回文子串、LC 345 反转字符串中的元音字母、LC 11 盛最多水的容器。
