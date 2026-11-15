---
slug: find-substring-with-given-hash-value
---
## Q
**LC 2156 查找给定哈希值的子串**｜Hard

字符串 `s` 的多项式哈希 `hash(s, power, modulo) = (val(s[0]) + val(s[1])·power + val(s[2])·power² + …) mod modulo`，其中 `val('a') = 1`。求 `s` 中第一个长度为 `k` 且哈希值等于 `hashValue` 的子串（保证存在）。

## A
**一句话。** 因为 `s[0]` 的权重是 `power⁰`，窗口左移时新字符直接作首位、旧的整体乘 `power`，所以从后往前滚动哈希；最后出现的满足条件的下标就是最靠左的答案。

```python
def sub_str_hash(s, power, modulo, k, hash_value):
    n = len(s)
    pk = pow(power, k, modulo)
    h = 0
    ans = -1
    for i in range(n - 1, -1, -1):
        h = (h * power + ord(s[i]) - 96) % modulo  # 新字符作首位
        if i + k < n:                              # 移出右端字符
            h = (h - (ord(s[i + k]) - 96) * pk) % modulo
        if i + k <= n and h == hash_value:
            ans = i                        # 继续往左，取最左
    return s[ans:ans + k]
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 从左往右滚动：新字符会落到权重最高的位置，要做逆元，从右往左就不用。
- 移出字符的权重写成 `power^(k-1)`：左移一位后它的权重变成了 `power^k`。
- 窗口不满 `k` 时就比较：要求 `i + k <= n`。

**追问。**
- 为什么不一发现就返回？：从右往左扫，先看到的是靠右的，最后一个匹配才是最靠左的。

**同模式。** LC 303 区域和检索 - 数组不可变、LC 3754 连接非零数字并乘以其数字和 I、LC 187 重复的DNA序列
