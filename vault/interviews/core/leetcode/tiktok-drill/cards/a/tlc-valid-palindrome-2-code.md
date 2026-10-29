---
id: tlc-valid-palindrome-2-code
node: a.valid-palindrome
type: qa
step: 2
---
## Q
**LC 125 验证回文串**｜Easy · 字节高频｜写出 Python 实现

字符串 `s`（`1 <= s.length <= 2 * 10^5`，可打印 ASCII）按「转小写并丢掉非字母数字字符」清洗之后，是不是回文串？要求 `O(n)` 时间，额外空间 `O(1)`。

## A
**思路。** 左右指针从两端向中间靠拢；每一轮先各自跳过非字母数字字符，再比较两个字符的小写形式，不等就立刻返回 `False`，走完则是回文。

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

**复杂度。** 时间 `O(n)`：每个指针只前进不后退，合计至多走 `n` 步；空间 `O(1)`。

**写法要点。** `str.isalnum()` 一次判断「字母或数字」，比手写区间比较清楚；`lower()` 放在比较处，不先整体转小写，所以不造新串；`left, right = left + 1, right - 1` 用元组赋值，两个指针同步移动。想要短版本可以写 `t = [c.lower() for c in s if c.isalnum()]; return t == t[::-1]`，正确但多 `O(n)` 空间，面试里作为第一版再优化到指针版。
