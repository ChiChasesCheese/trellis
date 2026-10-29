---
id: tlc-valid-palindrome-ii-2-code
node: b.valid-palindrome-ii
type: qa
step: 2
---
## Q
**LC 680 验证回文字符串 Ⅱ**｜写出 Python 实现

字符串 `s`（长度 `1 ~ 10^5`，全是小写字母）最多删一个字符，能不能变成回文串？要求 `O(n)` 时间。

## A
**思路。** 两个指针从两端向中间走，相等就同时内移；第一次不相等时，答案只取决于删 `s[left]` 后的区间 `[left+1, right]` 或删 `s[right]` 后的区间 `[left, right-1]` 是不是回文，各用一个下标版的 `is_pal` 判断，不拷贝字符串。

```python
def valid_palindrome(s: str) -> bool:
    def is_pal(i: int, j: int) -> bool:        # s[i..j]（闭区间）是不是回文
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:                # 第一次失配：删左边或删右边，各试一次
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True
```

运行：`"aba"` → `True`，`"abca"` → `True`，`"abc"` → `False`，`"aab"` → `True`，`"a"` → `True`，`"ab"` → `True`。

**复杂度。** 时间 `O(n)`：主循环最多走 `n/2` 步，失配后的两次 `is_pal` 各最多扫 `n/2` 个位置，且只会触发一次；空间 `O(1)`（用下标，不切片）。

**写法要点。** 内层函数 `is_pal(i, j)` 用下标而不切片：不复制字符串，空间 `O(1)`。`or` 短路：删左成立就不再判删右。失配后立刻 `return`，不需要计数器去记「已经删了几次」，「最多一次」直接由程序结构（只在第一次失配分叉）表达。切片写法 `(t := s[left+1:right+1]) == t[::-1]` 更短且在 C 里跑得快，但每次复制 `O(n)` 内存；先讲清下标版，再说切片版也可以。
