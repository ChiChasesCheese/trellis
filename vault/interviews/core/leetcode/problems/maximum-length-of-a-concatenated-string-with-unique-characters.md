---
slug: maximum-length-of-a-concatenated-string-with-unique-characters
---
## Q
**LC 1239 串联字符串的最大长度**｜Medium

从字符串数组 `arr` 中选若干个按序连接，要求所有字母各不相同，求最长长度。`arr.length <= 16`。

## A
**一句话。** 字符串压成 26 位字母掩码，维护「已能拼出的掩码集合」，与不相交的新串做并集。

```python
def max_length(arr):
    masks, best = {0}, 0
    for s in arr:
        if len(set(s)) < len(s):     # 自身有重复字母，不能选
            continue
        cur = 0
        for ch in s:
            cur |= 1 << (ord(ch) - 97)
        for m in list(masks):        # 拍快照，别边遍历边加
            if m & cur == 0:
                masks.add(m | cur)
                best = max(best, (m | cur).bit_count())
    return best
```

**复杂度。** 时间 `O(2^n)`，空间 `O(2^n)`。

**易错点。**
- 边遍历 `masks` 边往里加：抛 `RuntimeError: Set changed size during iteration`。
- 不过滤自带重复字母的串：`["aa","bb"]` 得 `2`，掩码把 `"aa"` 当一个字母，应为 `0`。

**追问。**
- 回溯写法？：`dfs(i, mask)` 选或不选第 `i` 个串，到末尾取 `mask.bit_count()`，可用剩余位数上界剪枝。
- 要返回具体字符串？：把 `masks` 换成字典 `mask -> 字符串`，合并时一起拼接。

**同模式。** LC 78 子集、LC 1255 得分最高的单词集合、LC 2002 两个回文子序列长度的最大乘积、LC 1178 猜字谜
