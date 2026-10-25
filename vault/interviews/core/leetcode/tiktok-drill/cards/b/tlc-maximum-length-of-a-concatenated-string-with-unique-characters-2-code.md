---
id: tlc-maximum-length-of-a-concatenated-string-with-unique-characters-2-code
node: b.maximum-length-of-a-concatenated-string-with-unique-characters
type: qa
step: 2
---
## Q
**LC 1239 串联字符串的最大长度**｜写出 Python 实现

字符串数组 `arr`（`1 <= arr.length <= 16`，每个串 `1` 到 `26` 个小写字母），选出若干个串按原顺序连接，要求结果中所有字母互不相同，返回可行结果的最大长度。

## A
**思路。** 用 26 位整数掩码表示字母集合。`masks` 集合记录目前所有可能的字母集合，初始只有空集 `0`。对每个内部无重复字母的串，算出它的掩码 `cur`，与每个不相交的旧掩码合并并加入集合，同时更新最大位数。

```python
def max_length(arr: list[str]) -> int:
    masks = {0}                                  # 所有"字母互不重复"的拼接能得到的字母集合
    best = 0
    for s in arr:
        if len(set(s)) < len(s):                 # 自己内部就有重复字母：永远不能选
            continue
        cur = 0
        for ch in s:
            cur |= 1 << (ord(ch) - 97)
        for m in list(masks):                    # 对旧集合拍快照，别边遍历边加
            if m & cur == 0:                     # 和 s 没有公共字母：可以拼上
                masks.add(m | cur)
                best = max(best, (m | cur).bit_count())
    return best
```

运行：`["un","iq","ue"]` → `4`；`["cha","r","act","ers"]` → `6`；`["abcdefghijklmnopqrstuvwxyz"]` → `26`；`["aa","bb"]` → `0`；`["a","a"]` → `1`。

**复杂度。** 时间最坏 `O(2^n)`：集合里最多 `2^n` 个掩码；空间 `O(2^n)`。

**写法要点。** 掩码用 `int` 即可，Python 整数没有位数限制；`m & cur == 0` 在 Python 里 `&` 的优先级高于 `==`，等价于 `(m & cur) == 0`（与 C 语言相反，C 里要加括号）；`int.bit_count()`（Python 3.10+）直接数 `1` 的个数；`list(masks)` 取快照，集合在遍历中不能改变大小；用 `set` 而不是 `list` 自动去掉由不同子集得到的相同掩码。
