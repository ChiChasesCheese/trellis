---
id: tlc-valid-palindrome-3-why
node: a.valid-palindrome
type: qa
step: 3
---
## Q
**LC 125 验证回文串**｜Easy · 字节高频｜正确性

双指针版本里，内层「跳过非字母数字」的循环为什么要带 `left < right`？判断字符为什么必须用 `isalnum()` 而不是 `isalpha()`？分别给出出错的输入。

## A
**不变量。** 每一轮开始时，`s[:left]` 和 `s[right + 1:]` 里的有效字符已经两两配对成功；剩下的 `s[left : right + 1]` 是还没验证的区间。每一轮取区间两端各一个有效字符比较，配对成功就把区间收窄。

**为什么要 `left < right`。** 跳过循环要保证指针不越过对方。若写成 `while not s[left].isalnum(): left += 1`，输入 `".,"` 时 `left` 一路走到下标 2，抛 `IndexError`；正确答案是 `True`（清洗后是空串）。加上 `left < right` 后指针相遇就停，外层循环结束，返回 `True`。

**为什么是 `isalnum()`。** 题面保留的是「字母和数字」。若用 `isalpha()`，数字被当成无效字符丢掉：`"0P"` 清洗成 `"p"`，判成 `True`；正确清洗结果是 `"0p"`，答案 `False`。
