---
slug: find-the-difference
---
## Q
**LC 389 找不同**｜Easy

`t` 是 `s` 重排后再随机插入一个小写字母得到的，找出被插入的那个字母。

## A
**一句话。** 把 `s` 和 `t` 所有字符一起异或，成对抵消，只剩多出来的字母。

```python
def find_the_difference(s, t):
    x = 0
    for ch in chain(s, t):    # 不拼接 s + t，省临时字符串
        x ^= ord(ch)
    return chr(x)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 用集合差 `set(t) - set(s)`：`s="a"`、`t="aa"` 得空集，要按次数而不是种类。
- 忘记 `chr`：异或结果是整数，不是字母。

**追问。**
- 不用异或还能怎么做？：求和版 `chr(sum(map(ord, t)) - sum(map(ord, s)))`，或 `Counter(t) - Counter(s)`。
- 落单的不止一个（LC 260）？：先按异或结果的最低位把数分成两组。

**同模式。** LC 136 只出现一次的数字、LC 268 丢失的数字、LC 260 只出现一次的数字 III、LC 242 有效的字母异位词
