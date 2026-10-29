---
id: tlc-reverse-words-in-a-string-4-followup
node: a.reverse-words-in-a-string
type: qa
step: 4
---
## Q
**LC 151 反转字符串中的单词**｜追问

面试官接着问：（1）字符串可变（字符数组）时，如何 `O(1)` 额外空间原地完成？（2）为什么「整体反转再逐词反转」是对的？（3）只想反转每个单词里的字母、单词顺序保持不变呢？

## A
1. **原地三步**（用列表模拟可变字符数组）：压缩空格（读写双指针，去掉首尾空格并让单词间只留一个）；整体反转；再按空格切出每个单词各自反转回来。

```python
def reverse_words_inplace(chars: list[str]) -> None:
    def reverse(lo: int, hi: int) -> None:         # 反转 chars[lo:hi]
        hi -= 1
        while lo < hi:
            chars[lo], chars[hi] = chars[hi], chars[lo]
            lo, hi = lo + 1, hi - 1

    write = 0                                      # 1. 压缩空格：去掉首尾空格，单词间只留一个
    for ch in chars:
        if ch != " " or (write and chars[write - 1] != " "):
            chars[write] = ch
            write += 1
    if write and chars[write - 1] == " ":
        write -= 1
    del chars[write:]
    reverse(0, write)                              # 2. 整体反转
    start = 0
    for end in range(write + 1):                   # 3. 逐个单词再反转回来
        if end == write or chars[end] == " ":
            reverse(start, end)
            start = end + 1
```

`list("  hello world  ")` 处理后是 `"world hello"`，`list("a good   example")` 处理后是 `"example good a"`。
2. **为什么对**：整体反转把单词顺序倒过来，但每个单词里的字母也被倒了；每个单词各自再反转一次，字母恢复，单词顺序保持倒过来。两次反转抵消在单词内部，只留下单词顺序的改变。这与 LC 189「轮转数组」的三次反转是同一个技巧。
3. **只反转单词内部**（LC 557）：不需要整体反转，按空格切出每个单词各自反转即可；Python 里 `" ".join(w[::-1] for w in s.split(" "))`。

**Python 提醒**：Python 的 `str` 不可变，真正的 `O(1)` 空间原地反转只对 `list[str]`（或 `bytearray`）成立；`del chars[write:]` 用来丢掉压缩后多出的尾部，在 C / Java 里这一步是记录新长度。
