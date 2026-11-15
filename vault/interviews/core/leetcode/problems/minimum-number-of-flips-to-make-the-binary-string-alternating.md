---
slug: minimum-number-of-flips-to-make-the-binary-string-alternating
---
## Q
**LC 1888 使二进制字符串字符交替的最少反转次数**｜Medium

二进制字符串 `s` 有两种操作：①把第一个字符移到末尾（不计代价）；②翻转任意一个字符。求让 `s` 变成交替串（`0101…` 或 `1010…`）所需的最少翻转次数。

## A
**一句话。** 操作 ① 相当于在 `s + s` 上取长度为 `n` 的窗口；滑动窗口维护"与 `0101…` 不同的位数" `diff`，另一种模式的代价是 `n - diff`。

```python
def min_flips(s):
    n = len(s)
    t = s + s
    diff = 0                       # 窗口与 0101... 不同的位数
    ans = n
    for i, c in enumerate(t):
        if int(c) != i % 2:
            diff += 1
        if i >= n:                 # 窗口左端滑出
            if int(t[i - n]) != (i - n) % 2:
                diff -= 1
        if i >= n - 1:
            ans = min(ans, diff, n - diff)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只算一种目标串：窗口要同时比较 `diff` 和 `n - diff`，`0101…` 与 `1010…` 都可能更省。
- 左端滑出时下标用 `i`：要用被移出的位置 `i - n` 的奇偶。

**追问。**
- 偶数长度也要拼两遍吗？：不必。偶数长度旋转一位只是把 `diff` 与 `n - diff` 互换，已被 `min` 覆盖；奇数长度旋转才会带来新的代价。

**同模式。** LC 1653 使字符串平衡的最少删除次数、LC 2483 商店的最少代价、LC 926 将字符串翻转到单调递增
