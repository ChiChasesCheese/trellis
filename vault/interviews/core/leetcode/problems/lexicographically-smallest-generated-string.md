---
slug: lexicographically-smallest-generated-string
---
## Q
**LC 3474 字典序最小的生成字符串**｜Hard

`str1` 由 `'T'`/`'F'` 组成（长 `n`），`str2` 长 `m`。求长 `n+m-1` 的最小字符串 `word`：`str1[i]=='T'` 时 `word[i:i+m]==str2`，`'F'` 时不等；无解返回 `""`。

## A
**一句话。** 先铺所有 `'T'` 窗口，自由位填 `'a'`；再对恰好等于 `str2` 的 `'F'` 窗口，把最右的自由位改成 `'b'`。

```python
def generate_string(str1, str2):
    n, m = len(str1), len(str2)
    word = [None] * (n + m - 1)      # None：还没被 'T' 钉死
    for i, flag in enumerate(str1):
        if flag != "T":
            continue
        for j, ch in enumerate(str2):
            if word[i + j] not in (None, ch):
                return ""            # 重叠处冲突
            word[i + j] = ch
    forced = [ch is not None for ch in word]
    res = [ch or "a" for ch in word]   # 自由位先填 'a'
    for i, flag in enumerate(str1):
        if flag == "F" and res[i:i + m] == list(str2):
            # 改最右的自由位，对字典序伤害最小
            for j in range(i + m - 1, i - 1, -1):
                if not forced[j]:
                    res[j] = "b"
                    break
            else:
                return ""            # 窗口全被钉死
    return "".join(res)
```

**复杂度。** 时间 `O(nm)`，空间 `O(n+m)`。

**易错点。**
- 铺 `'T'` 不查重叠冲突：`("TT","ab")` 得 `"aab"`，应为 `""`。
- 改最左的自由位：`("F","aa")` 得 `"ba"`，应为 `"ab"`。
- 改了被钉死的位：会破坏 `'T'` 窗口，`("TFT","aa")` 须返回 `""`。

**追问。**
- `m` 很大时窗口比较太慢？：用滚动哈希或 Z 函数 `O(1)` 比较。
- 怎么验证答案？：写按位回溯的暴力在小数据上对照。

**同模式。** LC 767 重构字符串、LC 316 去除重复字母、LC 936 戳印序列、LC 1202 交换字符串中的元素
