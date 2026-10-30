---
id: tlc-valid-palindrome-0-whole
node: b.valid-palindrome
type: qa
---
## Q
**LC 125 验证回文串**｜Easy · CodeTop 国内累计 14 次 · 最近 2026-04-25（国内 CodeTop）

把所有大写字母转成小写、并移除所有非字母数字字符之后，字符串正着读和反着读都一样，就称它是回文串（空串也算）。给字符串 `s`，判断它是不是回文串。`1 <= s.length <= 2 * 10^5`，`s` 只由可打印的 ASCII 字符组成。例：`"A man, a plan, a canal: Panama"` → `true`（清洗后是 `"amanaplanacanalpanama"`），`"race a car"` → `false`，`" "` → `true`（清洗后是空串）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 双指针从两端向中间走：各自跳过非字母数字字符，再忽略大小写比较，不相等就返回 `False`；不构造清洗后的新字符串，`O(n)` 时间、`O(1)` 额外空间。

**识别。** 「正着读等于反着读」就是回文，标准工具是**两端向中间的双指针**：第 `i` 个字符必须等于倒数第 `i` 个。题面多出「忽略大小写、忽略符号」两个清洗条件，可以先清洗再判，也可以在指针移动时顺手跳过。`n = 2 * 10^5` 要求线性。

**推导。** 暴力：清洗成新串 `t`，判断 `t == t[::-1]`，`O(n)` 时间但要 `O(n)` 额外空间，正确，是可以先说出口的第一版。浪费：清洗和反转各造了一份拷贝。洞察：回文只要求「第 `i` 个有效字符」等于「倒数第 `i` 个有效字符」，所以把清洗内联进双指针，遇到无效字符就走过去；一趟扫描、不开新串。

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():    # 跳过非字母数字
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():          # 逐个比较，忽略大小写
            return False
        left, right = left + 1, right - 1
    return True
```

运行：`"A man, a plan, a canal: Panama"` → `True`，`"race a car"` → `False`，`" "` → `True`，`"0P"` → `False`，`".,"` → `True`。

**复杂度。** 时间 `O(n)`：两个指针合计最多走 `n` 步；空间 `O(1)`。

**易错点。**
- 内层 `while` 必须带 `left < right`：去掉后，全是符号的串 `".,"` 会让指针越界，抛 `IndexError`。
- 判断字符用 `isalnum()`，不能用 `isalpha()`：后者会把数字也丢掉，`"0P"` 被清洗成 `"p"` 而判成 `True`（正确答案 `False`）。
- 空串或全符号串是回文，返回 `True`，不要当成非法输入。

**追问。**
- 最多删掉一个字符后能否成回文（LC 680）：第一次不等时，分别试「跳过左边」「跳过右边」，各判一次剩下的区间。
- 输入含 Unicode：`isalnum()` 认 Unicode 字母，大小写折叠改用 `casefold()`。
- 输入是单链表（LC 234）：快慢指针找中点，反转后半段再逐个比较。

**同模式。** LC 680 验证回文串 II、LC 5 最长回文子串、LC 234 回文链表、LC 9 回文数。
