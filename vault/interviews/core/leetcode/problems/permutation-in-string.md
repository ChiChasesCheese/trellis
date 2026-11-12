---
slug: permutation-in-string
---
## Q
**LC 567 字符串的排列**｜Medium

判断 `s2` 是否包含 `s1` 的某个排列作为子串（只含小写字母）。

## A
**一句话。** 定长滑动窗口，维护 26 个字母的计数差和「计数差非零的字母种数」`diff`，`diff == 0` 即是排列。

```python
def check_inclusion(s1, s2):
    m = len(s1)
    if m > len(s2):
        return False
    cnt = [0] * 26                # s1 计数 - 窗口计数
    for a, b in zip(s1, s2):      # 装满第一个窗口
        cnt[ord(a) - 97] += 1
        cnt[ord(b) - 97] -= 1
    diff = sum(c != 0 for c in cnt)
    for i in range(m, len(s2)):
        if diff == 0:
            return True
        for ch, d in (s2[i], -1), (s2[i - m], 1):  # 进一个出一个
            k = ord(ch) - 97
            diff -= cnt[k] != 0
            cnt[k] += d
            diff += cnt[k] != 0
    return diff == 0              # 别漏最后一个窗口
```

**复杂度。** 时间 `O(m+n)`，空间 `O(1)`。

**易错点。**
- 只比字符集合：`s1="aab"`、`s2="abbcc"` 误判 `True`。
- 用字符码之和当指纹：`"ad"` 与 `"bc"`（`97+100 == 98+99`）冲突。
- 漏查最后一个窗口：`s1="ab"`、`s2="eidba"` 返回 `False`。

**追问。**
- 返回所有匹配起点（LC 438）？：每次 `diff == 0` 记录 `i - m`（循环内窗口起点按右端点换算）。
- 字符集很大？：`cnt` 换成 `Counter`，`diff` 逻辑不变。

**同模式。** LC 438 找到字符串中所有字母异位词、LC 76 最小覆盖子串、LC 30 串联所有单词的子串、LC 242 有效的字母异位词
